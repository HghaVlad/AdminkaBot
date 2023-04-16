from aiogram.dispatcher.filters import Filter
from aiogram.types import Message
from base_req import selectrole


class IsLogin(Filter):
    async def check(self, message: Message):
        username = selectrole(message.chat.id)
        return username is not None


class IsNotLogin(Filter):
    async def check(self, message: Message):
        username = selectrole(message.chat.id)
        return username is None


class IsTarget(Filter):
    async def check(self, message: Message):
        user_role = selectrole(message.chat.id)
        return user_role[0] == "Target"
