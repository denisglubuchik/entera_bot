from aiogram import F, Router
from aiogram.types import (Message, CallbackQuery, 
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from states.states import FillTemplate
from filters.filters import IsDate, IsEmails
from lexicon.lexicon_ru import BOT_LEXICON


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
async def cancel_command_state(message: Message):
    pass


@router.message(Command(commands='new_message')) #добавить клаву с выбором темплейта
async def new_message_command(message: Message):
    await message.answer(text=BOT_LEXICON['new_message'],
                         reply_markup=...)


# @router.callback_query(StateFilter(FillTemplate.choose_template), ...)
# async def choose_template(callback: CallbackQuery):
#     pass


# @router.message(StateFilter(FillTemplate.fill_start_time), IsDate())
# async def start_time_sent(message: Message):
#     pass


# @router.message(StateFilter(FillTemplate.fill_start_time))
# async def not_start_date(message: Message):
#     pass


# @router.message(StateFilter(FillTemplate.fill_end_time), IsDate()) #добавить клаву российским/иностранным
# async def end_time_sent(message: Message):
#     pass


# @router.message(StateFilter(FillTemplate.fill_end_time))
# async def not_end_date(message: Message):
#     pass


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
