from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon.lexicon_ru import BOT_LEXICON
from db import SyncOrm


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


@router.message(Command(commands='show_active_messages'), StateFilter(default_state))
async def show_active_messages_command(message: Message):
    messages = SyncOrm.select_active_messages()
    if messages:
        for mes in messages:
            await message.answer(
                text=f'Название: {mes.title}\n'
                     f'Дата начала: {mes.start_date}\n'
                     f'Дата конца: {mes.finish_date}\n'
                     f'Иностранным: {mes.foreign}\n'
                     f'Триальным: {mes.show_to_trial}\n'
                     f'include emails: '
                     f'{mes.include_emails if mes.include_emails is not None else "Всем"}\n'
                     f'exclude emails: '
                     f'{mes.exclude_emails if mes.exclude_emails is not None else "Нет"}'
            )
    else:
        await message.answer(BOT_LEXICON['no_active_messages'])

