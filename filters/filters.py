from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from datetime import datetime


class IsAdmin(BaseFilter):
    pass


class IsDate(BaseFilter):
    async def __call__(self, message: Message):
        date = message.text.strip('" ')
        pattern_date = '%Y-%m-%d %H:%M'
        try:
            datetime.strptime(date, pattern_date)
        except ValueError:
            return False
        return True


class IsEmails(BaseFilter):
    pass


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        return callback.data.isdigit()