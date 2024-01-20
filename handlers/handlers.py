from aiogram import F, Router
from aiogram.types import (Message, CallbackQuery, 
                           InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from states.states import FillTemplate
from filters.filters import IsDate, IsEmails, IsDigitCallbackData
from lexicon.lexicon_ru import BOT_LEXICON
from db.db import templates_db
from keyboards.keyboards import create_templates_kb


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
    for template in templates_db:
        await message.answer(text=f'<b>Шаблон {template}</b>\n'
                            f'{templates_db[template]}')


@router.message(Command(commands='new_message'), StateFilter(default_state)) #добавить клаву с выбором темплейта
async def new_message_command(message: Message, state: FSMContext):
    await message.answer(text=BOT_LEXICON['new_message'],
                         reply_markup=create_templates_kb(*templates_db))
    await state.set_state(FillTemplate.choose_template)


@router.callback_query(StateFilter(FillTemplate.choose_template),
                       IsDigitCallbackData())
async def choose_template(callback: CallbackQuery, state: FSMContext):
    await state.update_data(template=callback.data)
    await callback.message.edit_text(
        text=f'Вы выбрали шаблон {callback.data}',
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


@router.message(StateFilter(FillTemplate.fill_end_time), IsDate()) #добавить клаву российским/иностранным (true если иностранным)
async def end_time_sent(message: Message, state: FSMContext):
    await state.update_data(end_time=message.text.strip('" '))
    await message.answer(text=BOT_LEXICON['russian/foreign'])


@router.message(StateFilter(FillTemplate.fill_end_time))
async def not_end_date(message: Message):
    await message.answer(text=BOT_LEXICON['not_date'])


# @router.callback_query(StateFilter(FillTemplate.fill_where_users_from), ...) #добавить клаву про триальных юзеров
# async def where_users_from(callback: CallbackQuery):
#     pass


# @router.callback_query(StateFilter(FillTemplate.fill_trial_users), ...)
# async def trial_users(callback: CallbackQuery):
#     pass


# @router.message(StateFilter(FillTemplate.fill_include_emails), IsEmails)
# async def include_emails(message: Message):
#     pass


# @router.message(StateFilter(FillTemplate.fill_include_emails))
# async def not_include_emails(message: Message):
#     pass


# @router.message(StateFilter(FillTemplate.fill_exclude_emails), IsEmails)
# async def exclude_emails(message: Message):
#     pass


# @router.message(StateFilter(FillTemplate.fill_exclude_emails))
# async def not_exclude_emails(message: Message):
#     pass
