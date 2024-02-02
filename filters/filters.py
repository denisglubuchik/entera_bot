import uuid

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from datetime import datetime
from email_validate import validate


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
        return {'date': date}


class IsEmails(BaseFilter):
    async def __call__(self, message: Message):
        if message.text.lower().strip() == 'всем':
            return {'email': 'всем'}
        if message.text.lower().strip() == 'нет':
            return {'email': 'нет'}
        emails = message.text.split(', ')
        for email in emails:
            if not validate(
                email_address=email.strip(),
                check_format=True,
                check_blacklist=False,
                check_dns=False,
                dns_timeout=10,
                check_smtp=False,
                smtp_debug=False
            ):
                return False
        return {'email': emails}


class IsUUID(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        uuid_to_valid = callback.data
        try:
            uuid_obj = uuid.UUID(uuid_to_valid, version=4)
        except ValueError:
            return False
        return True


class IsDelTemplate(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        return callback.data.endswith('del')
