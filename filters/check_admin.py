from typing import Union

from aiogram.filters import BaseFilter

from database.admin_operations import AdminOperations

from aiogram.types import Message, CallbackQuery

from logger import logger


class CheckAdminDefault(BaseFilter):

    def __init__(self, sqlbase: AdminOperations):
        self.sqlbase = sqlbase

    async def __call__(self, message_or_callback: Union[Message, CallbackQuery]) -> bool:
        await self.sqlbase.connect()
        password_and_user = await self.sqlbase.select_password_and_user()
        await self.sqlbase.close()
        if isinstance(message_or_callback, Message):
            logger.info(f"{password_and_user}; {message_or_callback.chat.id} Использовал Router для админов")
            if password_and_user[1] == str(message_or_callback.chat.id):
                return True
            else:
                return False
        else:
            logger.info(f"{password_and_user}; {message_or_callback.message.chat.id} Использовал Router для админов")
            if password_and_user[1] == str(message_or_callback.message.chat.id):
                return True
            else:
                return False