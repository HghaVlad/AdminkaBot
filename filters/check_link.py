from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class Islink(BoundFilter):
    async def check(self, message: Message):
        return len(message.text.split()) == 2 and message.text.split()[0] == '/start'


class IsReglink(BoundFilter):
    async def check(self, message: Message):
        return message.text.split()[1][0:3] == 'reg'


class IsNewpasslink(BoundFilter):
    async def check(self, message: Message):
        return message.text.split()[1][0:4] == 'pass'
