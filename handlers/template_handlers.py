from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from states.states import Template
from filters.filters import IsUUID, IsDelTemplate
from lexicon.lexicon_ru import BOT_LEXICON
from keyboards import (create_save_template_kb, create_edit_template_kb,
                       create_templates_kb)
from db import SyncOrm


router = Router()


@router.message(Command(commands='templates'), StateFilter(default_state))
async def templates_command(message: Message):
    templates = SyncOrm.select_templates()
    if templates:
        for template in templates:
            await message.answer(text=f'Шаблон {template[1]}\n'
                                      f'{template[2]}')
    else:
        await message.answer('Шаблонов нет')


@router.message(Command(commands='new_template'), StateFilter(default_state))
async def new_template_command(message: Message, state: FSMContext):
    await message.answer(text=BOT_LEXICON['new_template_title'])
    await state.set_state(Template.fill_title)


@router.message(StateFilter(Template.fill_title))
async def new_template_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Template.fill_content)
    await message.answer(text=BOT_LEXICON['new_template_content'])


@router.message(StateFilter(Template.fill_content))
async def new_template_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    template = await state.get_data()
    await state.set_state(Template.accept_template)
    await message.answer(text=f'{template["title"]}\n'
                              f'{template["content"]}',
                         reply_markup=create_save_template_kb())


@router.callback_query(StateFilter(Template.accept_template),
                       F.data.in_(['1', '0']))
async def new_template_accept(callback: CallbackQuery, state: FSMContext):
    if callback.data == '1':
        template = await state.get_data()
        SyncOrm.insert_new_template(template)
        await callback.message.edit_text(text=BOT_LEXICON['new_template_success'])
    else:
        await callback.message.edit_text(text=BOT_LEXICON['new_template_cancel'])
    await state.clear()


@router.message(Command(commands='edit_templates'), StateFilter(default_state))
async def edit_templates_command(message: Message, state: FSMContext):
    templates = SyncOrm.select_templates()
    await message.answer(text=BOT_LEXICON['edit_templates_command'],
                         reply_markup=create_templates_kb(*templates, edit=True))
    await state.set_state(Template.edit_templates)


@router.callback_query(F.data == 'edit_templates', StateFilter(Template.edit_templates))
async def edit_templates(callback: CallbackQuery):
    templates = SyncOrm.select_templates()
    await callback.message.edit_reply_markup(reply_markup=create_edit_template_kb(*templates))


@router.callback_query(F.data == 'cancel_edit_templates', StateFilter(Template.edit_templates))
async def cancel_edit_templates(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Вы завершили редактирование')
    await callback.answer()
    await state.clear()


@router.callback_query(IsDelTemplate(), StateFilter(Template.edit_templates))
async def del_template(callback: CallbackQuery, state: FSMContext):
    uuid = callback.data[:-3]
    SyncOrm.delete_template(uuid)
    templates = SyncOrm.select_templates()
    if templates:
        await callback.message.edit_reply_markup(reply_markup=create_edit_template_kb(*templates))
    else:
        await callback.message.edit_text(text='Шаблонов больше нет')
        await state.clear()


@router.callback_query(IsUUID(), StateFilter(Template.edit_templates))
async def do_nothing(callback: CallbackQuery):
    await callback.answer()
