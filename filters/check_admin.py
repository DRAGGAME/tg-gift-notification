from typing import Union

from aiogram.filters import BaseFilter

from database.admin_operations import AdminOperations

from aiogram.types import Message

from logger import logger


class CheckAdmin(BaseFilter):

    def __init__(self, sqlbase: AdminOperations):
        self.sqlbase = sqlbase

    async def __call__(self, message: Message) -> Union[bool, dict]:
        await self.sqlbase.connect()
        password_and_user = await self.sqlbase.select_password_and_user()
        await self.sqlbase.close()
        logger.info(f"{password_and_user}; {message.chat.id}")
        if password_and_user[1] == message.chat.id:
            return False

        elif password_and_user[0]:
            return True
        else:
            return False
