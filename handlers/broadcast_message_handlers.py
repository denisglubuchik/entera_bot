from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from states.states import FillTemplate
from lexicon.lexicon_ru import BOT_LEXICON
from filters.filters import IsUUID, IsDate, IsEmails
from keyboards import (create_templates_kb, create_rus_for_kb,
                       create_trial_kb, create_new_or_template_kb,
                       create_save_message_kb)
from db import SyncOrm


router = Router()


async def is_template(state: FSMContext) -> bool:
    data = await state.get_data()
    if 'template' not in data:
        return True
    return False


@router.message(Command(commands='new_message'), StateFilter(default_state))
async def new_message_command(message: Message, state: FSMContext):
    await message.answer(text=BOT_LEXICON['new_message'],
                         reply_markup=create_new_or_template_kb())
    await state.set_state(FillTemplate.new_or_template)


@router.callback_query(F.data == 'template', StateFilter(FillTemplate.new_or_template))
async def choose_template(callback: CallbackQuery, state: FSMContext):
    templates = SyncOrm.select_templates()
    await callback.message.edit_text(text=BOT_LEXICON['choose_template'],
                                     reply_markup=create_templates_kb(*templates))
    await state.set_state(FillTemplate.choose_template)
    await callback.answer()


@router.callback_query(F.data == 'back', StateFilter(FillTemplate.new_or_template))
async def back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=BOT_LEXICON['new_message'],
                                     reply_markup=create_new_or_template_kb())
    await state.set_state(FillTemplate.new_or_template)


@router.callback_query(F.data == 'new', StateFilter(FillTemplate.new_or_template))
async def fill_title(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Вы создаете новое сообщение')
    await callback.message.answer(text=BOT_LEXICON['title'])
    await state.set_state(FillTemplate.fill_title)


@router.message(StateFilter(FillTemplate.fill_title))
async def get_title_fill_content(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text=BOT_LEXICON['content'])
    await state.set_state(FillTemplate.fill_content)


@router.message(StateFilter(FillTemplate.fill_content))
async def get_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    await state.set_state(FillTemplate.fill_start_time)
    await message.answer(text=BOT_LEXICON['start_show'])


@router.callback_query(StateFilter(FillTemplate.choose_template),
                       IsUUID())
async def choose_template_answer(callback: CallbackQuery, state: FSMContext):
    await state.update_data(template=callback.data)
    template = SyncOrm.select_template_by_id(callback.data)[0]
    await callback.message.edit_text(
        text=f'Вы выбрали шаблон \n{template}',
    )
    await state.set_state(FillTemplate.fill_start_time)
    await callback.message.answer(text=BOT_LEXICON['start_show'])


@router.message(StateFilter(FillTemplate.fill_start_time), IsDate())
async def start_time_sent(message: Message, state: FSMContext, date: str):
    await state.update_data(start_time=date)
    await message.answer(text=BOT_LEXICON['end_show'])
    await state.set_state(FillTemplate.fill_end_time)


@router.message(StateFilter(FillTemplate.fill_start_time))
async def not_start_date(message: Message):
    await message.answer(text=BOT_LEXICON['not_date'])


@router.message(StateFilter(FillTemplate.fill_end_time), IsDate())
async def end_time_sent(message: Message, state: FSMContext, date: str):
    await state.update_data(end_time=date)
    await message.answer(text=BOT_LEXICON['russian/foreign'],
                         reply_markup=create_rus_for_kb())
    await state.set_state(FillTemplate.fill_where_users_from)


@router.message(StateFilter(FillTemplate.fill_end_time))
async def not_end_date(message: Message):
    await message.answer(text=BOT_LEXICON['not_date'])


@router.callback_query(StateFilter(FillTemplate.fill_where_users_from),
                       F.data.in_(['1', '0']))  # true or false
async def where_users_from(callback: CallbackQuery, state: FSMContext):
    await state.update_data(foreign=bool(int(callback.data)))
    await callback.message.edit_text(
        text=f'Вы выбрали показывать '
        f'{"иностранным" if callback.data == "True" else "российским"}'
        ' пользователям'
    )
    await callback.message.answer(text=BOT_LEXICON['trial'],
                                  reply_markup=create_trial_kb())
    await state.set_state(FillTemplate.fill_trial_users)


@router.callback_query(StateFilter(FillTemplate.fill_trial_users),
                       F.data.in_(['1', '0']))  # true or false
async def trial_users(callback: CallbackQuery, state: FSMContext):
    await state.update_data(trial=bool(int(callback.data)))
    await callback.message.edit_text(
        text=f'Вы выбрали {"не" if callback.data == "False" else ""}'
        ' показывать триальным пользователям'
    )
    await callback.message.answer(text=BOT_LEXICON['include_emails'])
    await state.set_state(FillTemplate.fill_include_emails)


@router.message(StateFilter(FillTemplate.fill_include_emails), IsEmails())
async def include_emails(message: Message, state: FSMContext, email: list | str):
    if email != 'всем':
        await state.update_data(include_emails=email,
                                exclude_emails=None)

        await  state.set_state(FillTemplate.fill_save_or_not)
        save_and_send = await is_template(state)
        await message.answer(text=BOT_LEXICON['save'],
                             reply_markup=create_save_message_kb(save_and_send=save_and_send))
    else:
        await state.update_data(include_emails=None)
        await message.answer(text=BOT_LEXICON['exclude_emails'])
        await state.set_state(FillTemplate.fill_exclude_emails)


@router.message(StateFilter(FillTemplate.fill_include_emails))
async def not_include_emails(message: Message):
    await message.answer(text=BOT_LEXICON['not_email'])


@router.message(StateFilter(FillTemplate.fill_exclude_emails), IsEmails())
async def exclude_emails(message: Message, state: FSMContext, email: list | str):
    if email != 'нет':
        await state.update_data(exclude_emails=email)
    else:
        await state.update_data(exclude_emails=None)

    await  state.set_state(FillTemplate.fill_save_or_not)
    save_and_send = await is_template(state)
    await message.answer(text=BOT_LEXICON['save'],
                         reply_markup=create_save_message_kb(save_and_send=save_and_send))


@router.message(StateFilter(FillTemplate.fill_exclude_emails))
async def not_exclude_emails(message: Message):
    await message.answer(text=BOT_LEXICON['not_email'])


@router.callback_query(StateFilter(FillTemplate.fill_save_or_not),
                F.data.in_(['send_message', 'save_template_send', 'cancel']))
async def save_or_not(callback: CallbackQuery, state: FSMContext):
    new_message = await state.get_data()
    if callback.data == 'send_message':
        SyncOrm.insert_new_message(new_message)
        await callback.message.edit_text(text=BOT_LEXICON['successful_end'])
    elif callback.data == 'save_template_send':
        SyncOrm.insert_new_template(template={
            'title': new_message['title'],
            'content': new_message['content']
        })
        SyncOrm.insert_new_message(new_message)
        await callback.message.edit_text(text=BOT_LEXICON['successful_end'])
    else:
        await callback.message.edit_text(text='Отмена')
    await state.clear()
    await callback.answer()
