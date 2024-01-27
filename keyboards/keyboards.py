from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_templates_kb(*args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=str(button[1]),
            callback_data=str(button[0])
        ), width=2)
    return kb_builder.as_markup()


def create_rus_for_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(
        text='Российским',
        callback_data='0'  # false
    ), InlineKeyboardButton(
        text='Иностранным',
        callback_data='1'  # true
    ), width=2)

    return kb_builder.as_markup()


def create_trial_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(
        text='Да',
        callback_data='1'  # true
    ), InlineKeyboardButton(
        text='Нет',
        callback_data='0'  # false
    ), width=2)

    return kb_builder.as_markup()
