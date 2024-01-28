from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import BOT_LEXICON


def create_templates_kb(*args, edit=None) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=str(button[1]),
            callback_data=str(button[0])
        ), width=2)

    if edit:
        kb_builder.row(InlineKeyboardButton(
            text=BOT_LEXICON['edit_templates_button'],
            callback_data='edit_templates'
        ), InlineKeyboardButton(
            text=BOT_LEXICON['cancel_edit_templates'],
            callback_data='cancel_edit_templates'
        ), width=2)
    return kb_builder.as_markup()


def create_edit_template_kb(*args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{BOT_LEXICON["del"]}{str(button[1])}',
            callback_data=f'{str(button[0])}del'
        ), width=2)
    kb_builder.row(InlineKeyboardButton(
        text=BOT_LEXICON['finish_edit_templates'],
        callback_data='cancel_edit_templates'
    ))
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


def create_save_template_kb() ->InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Сохранить',
            callback_data='1'
        ), InlineKeyboardButton(
            text='Отмена',
            callback_data='0'
        ), width=2
    )
    return kb_builder.as_markup()
