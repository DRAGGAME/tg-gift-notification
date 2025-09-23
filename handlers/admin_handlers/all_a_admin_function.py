import apscheduler
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message

from database.admin_operations import AdminOperations
from filters.check_admin import CheckAdmin

from keyboards.menu_fabric import FabricInline
router_for_admin = Router()
sqlbase_for_admin_function = AdminOperations()
keyboard = FabricInline()


class SetupFSM(StatesGroup):
    setup_password = State()


@router_for_admin.message(Command(commands=["setup", "Setup"]), CheckAdmin(sqlbase_for_admin_function))
async def setup_handler(message: Message, state: FSMContext):
    await sqlbase_for_admin_function.connect()
    password = await sqlbase_for_admin_function.select_password_and_user()
    if password:
        await state.clear()
        await state.update_data(password=password[0])
        await state.set_state(SetupFSM.setup_password)
        await message.answer("Войдите для начала работы.\nP.S Пароль единоразовый для одного аккаунта\nВведите пароль:")
    else:
        await state.clear()
        await message.answer("Пароля - не существует, видимо, администратор уже существует\nВведите команду и пароль заново")

@router_for_admin.message(SetupFSM.setup_password)
async def setup_from_password_handler(message: Message, state: FSMContext):
    if message.text:
        password = await state.get_value("password")
        if message.text == password:
            await sqlbase_for_admin_function.update_admin_password(str(message.chat.id))
            await state.clear()
            await message.answer("Пароль - верный, вы зарегистрированы. Пароль - теперь недействителен")
        else:
            await state.clear()
            await message.answer("Пароль - неверный\nВведите команду и пароль заново")
    else:
        await state.clear()
        await message.answer("Это сообщение не текст\nВведите команду и пароль заново")
    await sqlbase_for_admin_function.close()




