from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.admin_operations import AdminOperations
from logger import logger


class CheckAdminSetup(BaseFilter):
    def __init__(self, sqlbase: AdminOperations):
        self.sqlbase = sqlbase

    async def __call__(self, message: Message) -> bool:
        admin = await self.sqlbase.select_admin_chat()
        if admin == "0":
            return True

        else:
            return False

