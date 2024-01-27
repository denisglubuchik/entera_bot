from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from states.states import FillTemplate, NewTemplate
from filters.filters import IsDate, IsEmails, IsUUID
from lexicon.lexicon_ru import BOT_LEXICON
from db.orm import SyncOrm
from keyboards.keyboards import (create_templates_kb, create_rus_for_kb,
                                 create_trial_kb)


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=BOT_LEXICON['start'])


@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(text=BOT_LEXICON['help'])


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def cancel_command_default(message: Message):
    await message.answer(text=BOT_LEXICON['cancel_default'])


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=BOT_LEXICON['cancel_state'])
    await state.clear()


@router.message(Command(commands='templates'), StateFilter(default_state))
async def templates_command(message: Message):
    templates = SyncOrm.select_templates()
    for template in templates:
        await message.answer(text=f'Шаблон {template[1]}\n'
                                  f'{template[2]}')


@router.message(Command(commands='new_template'), StateFilter(default_state))
async def new_template_command(message: Message, state: FSMContext):
    await message.answer(text=BOT_LEXICON['new_template_title'])
    await state.set_state(NewTemplate.fill_title)


@router.message(StateFilter(NewTemplate.fill_title))
async def new_template_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(NewTemplate.fill_content)
    await message.answer(text=BOT_LEXICON['new_template_content'])


@router.message(StateFilter(NewTemplate.fill_content))
async def new_template_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer(text=BOT_LEXICON['new_template_success'])
    template = await state.get_data()
    SyncOrm.insert_new_template(template)
    await state.clear()


@router.message(Command(commands='new_message'), StateFilter(default_state))
async def new_message_command(message: Message, state: FSMContext):
    templates = SyncOrm.select_templates()
    await message.answer(text=BOT_LEXICON['new_message'],
                         reply_markup=create_templates_kb(*templates))
    await state.set_state(FillTemplate.choose_template)


@router.callback_query(StateFilter(FillTemplate.choose_template),
                       IsUUID())
async def choose_template(callback: CallbackQuery, state: FSMContext):
    await state.update_data(template=callback.data)
    template = SyncOrm.select_template_by_id(callback.data)[0]
    await callback.message.edit_text(
        text=f'Вы выбрали шаблон \n{template}',
    )
    await state.set_state(FillTemplate.fill_start_time)
    await callback.message.answer(text=BOT_LEXICON['start_show'])


@router.message(StateFilter(FillTemplate.fill_start_time), IsDate())
async def start_time_sent(message: Message, state: FSMContext):
    await state.update_data(start_time=message.text.strip('" '))
    await message.answer(text=BOT_LEXICON['end_show'])
    await state.set_state(FillTemplate.fill_end_time)


@router.message(StateFilter(FillTemplate.fill_start_time))
async def not_start_date(message: Message):
    await message.answer(text=BOT_LEXICON['not_date'])


@router.message(StateFilter(FillTemplate.fill_end_time), IsDate())
async def end_time_sent(message: Message, state: FSMContext):
    await state.update_data(end_time=message.text.strip('" '))
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
async def include_emails(message: Message, state: FSMContext):
    if message.text.lower().strip() != 'всем':
        await state.update_data(include_emails=message.text.split(', '),
                                exclude_emails=None)
        new_message = await state.get_data()
        SyncOrm.insert_new_message(new_message)
        await state.clear()
        await message.answer(text=BOT_LEXICON['successful_end'])
    else:
        await state.update_data(include_emails=None)
        await message.answer(text=BOT_LEXICON['exclude_emails'])
        await state.set_state(FillTemplate.fill_exclude_emails)


@router.message(StateFilter(FillTemplate.fill_include_emails))
async def not_include_emails(message: Message):
    await message.answer(text=BOT_LEXICON['not_email'])


@router.message(StateFilter(FillTemplate.fill_exclude_emails), IsEmails())
async def exclude_emails(message: Message, state: FSMContext):
    if message.text.lower().strip() != 'нет':
        await state.update_data(exclude_emails=message.text.split(', '))
    else:
        await state.update_data(exclude_emails=None)

    new_message = await state.get_data()
    SyncOrm.insert_new_message(new_message)
    await state.clear()
    await message.answer(text=BOT_LEXICON['successful_end'])


@router.message(StateFilter(FillTemplate.fill_exclude_emails))
async def not_exclude_emails(message: Message):
    await message.answer(text=BOT_LEXICON['not_email'])


@router.message(Command(commands='show_message'), StateFilter(default_state))
async def show_message_command(message: Message):
    last_message = SyncOrm.select_last_message()
    await message.answer(
        text=f'Название: {last_message.title}\n'
             f'Дата начала: {last_message.start_date}\n'
             f'Дата конца: {last_message.finish_date}\n'
             f'Иностранным: {last_message.foreign}\n'
             f'Триальным: {last_message.show_to_trial}\n'
             f'include emails: '
             f'{last_message.include_emails if last_message.include_emails is not None else "Всем"}\n'
             f'exclude emails: '
             f'{last_message.exclude_emails if last_message.exclude_emails is not None else "Нет"}'
    )
