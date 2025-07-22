from collections.abc import AsyncIterator

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Text

from database.admin_operations import AdminOperations
from database.db import Sqlbase
from database.other_operations import OtherOperation
from keyboards.menu_fabric import FabricInline

keyboard_fabric = FabricInline()
router_for_stop = Router()
sqlbase = AdminOperations()


@router_for_stop.message(F.text.lower() == "стоп")
async def stop_message(message: Message, state: FSMContext):
    """
    Останавливает любой текущий процесс и возвращает в панель.
    """
    await sqlbase.connect()
    check_login = await sqlbase.check_login()
    if check_login:
        kb_new = await keyboard_fabric.inline_admin_main_menu()

        await message.answer(
            "Операция отменена\nПанель действий:",
            reply_markup=kb_new
        )
        await state.clear()

@router_for_stop.message(F.text=="Отправлять уведомления")
async def accept_answer(message: Message):
    await sqlbase.update_state(str(message.chat.id), True)
    await message.answer("Теперь вам отправляются уведомления о подарках ")

@router_for_stop.message(F.text=="Не отправлять уведомления")
async def accept_answer(message: Message):
    await sqlbase.update_state(str(message.chat.id), False)
    await message.answer("Теперь вам отправляются уведомления о подарках ")

