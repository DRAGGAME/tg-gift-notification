from aiogram.filters import BaseFilter

from database.admin_operations import AdminOperations

from aiogram.types import Message, CallbackQuery


class CheckAdmin(BaseFilter):
    """
    Проверка на админа
    """

    def __init__(self, sqlbase: AdminOperations):
        self.sqlbase = sqlbase

    async def __call__(self, message: Message) -> bool:
        admin = await self.sqlbase.select_admin_chat_id()
        if admin[0][0] == str(message.chat.id):
            return True
        else:
            return False


class CheckAdminCallback(BaseFilter):
    """
    Проверка на админа
    """

    def __init__(self, sqlbase: AdminOperations):
        self.sqlbase = sqlbase

    async def __call__(self, callback: CallbackQuery) -> bool:
        admin = await self.sqlbase.select_admin_chat_id()
        if admin[0][0] == str(callback.message.chat.id):
            return True
        else:
            return False