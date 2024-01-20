from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_templates_kb(*args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'Шаблон {button}',
            callback_data=str(button)
        ), width=2)
    return kb_builder.as_markup()