import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from config import bot
from database.admin_operations import AdminOperations
from filters.check_admin_for_setup import CheckAdminSetup
from keyboards.menu_fabric import FabricInline


class SetupFSM(StatesGroup):
    setup_password = State()


class SetupHandlers:
    def __init__(self):
        self.bot = bot

        self.router_setup = Router()

        self.admin_database = AdminOperations()

        self.admin_fabric_inline = FabricInline()

        self.register_start_handlers()

    def register_start_handlers(self):
        self.router_setup.message.register(self.setup_handler, CheckAdminSetup(self.admin_database), Command("setup"))
        self.router_setup.message.register(self.setup_from_password_handler, SetupFSM.setup_password,
                                     CheckAdminSetup(self.admin_database))

    async def setup_handler(self, message: Message, state: FSMContext):
        await state.clear()

        password = await self.admin_database.select_password_and_user()
        if password:
            await message.delete()

            await state.set_state(SetupFSM.setup_password)

            bot_msg = await message.answer(
                "Войдите для начала работы.\nP.S Пароль единоразовый для одного аккаунта\nВведите пароль:")

            await state.update_data(bot_msg=bot_msg.message_id)
        else:
            bot_msg = await message.answer(
                "Пароля - не существует, видимо, администратор уже существует")

            await asyncio.sleep(60)
            await bot_msg.delete()

    async def setup_from_password_handler(self, message: Message, state: FSMContext):
        msg_id = await state.get_value("bot_msg")
        await bot.delete_message(chat_id=message.chat.id, message_id=int(msg_id))

        if message.text:
            password = await self.admin_database.select_password_try(message.text)
            if password[0][0]:

                await message.delete()
                await self.admin_database.update_admin_password(str(message.chat.id))
                admin_keyboard = await self.admin_fabric_inline.inline_main_menu()

                await message.answer(
                    "Пароль - верный, вы зарегистрированы. Пароль - теперь недействителен\n\nЧто вы хотите сделать?",
                    reply_markup=admin_keyboard)
                await state.clear()

                return

            else:
                msg_bot_two = await message.answer("Пароль - неверный\nВведите команду /setup и пароль заново")
                await state.clear()

                await asyncio.sleep(30)
                await bot.delete_message(chat_id=message.chat.id, message_id=int(msg_bot_two.message_id))
        else:
            msg_bot_two = await message.answer("Это сообщение не текст\nВведите команду /setup и пароль заново")
            await state.clear()

            await asyncio.sleep(30)
            await bot.delete_message(chat_id=message.chat.id, message_id=int(msg_bot_two.message_id))
