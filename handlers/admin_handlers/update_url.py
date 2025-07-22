from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from pydantic import AnyWebsocketUrl

from database.admin_operations import AdminOperations
from handlers.admin_handlers.all_a_admin_function import router_for_admin
from keyboards.menu_fabric import InlineMainMenu, InlineAdminMenu, FabricInline

url_router = Router()
sqlbase_upgrade = AdminOperations()
keyboard_fabric_update = FabricInline()

class UrlPoliticEdit(StatesGroup):
    url = State()


class UrlUserEdit(StatesGroup):
    url = State()


class UrlPriceEdit(StatesGroup):
    price = State()


class DeleteFaq(StatesGroup):
    faq_num = State()


class AnswerFaq(StatesGroup):
    question = State()
    answer = State()


@url_router.callback_query(InlineAdminMenu.filter(F.action == "UrlUser"))
async def url_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UrlUserEdit.url)
    await callback.message.answer("Введите url")
    await callback.answer()


@url_router.message(UrlUserEdit.url)
async def url_edit_user(message: Message, state: FSMContext):
    if message.text:
        await sqlbase_upgrade.connect()
        await sqlbase_upgrade.update_url_user(message.text)
        await sqlbase_upgrade.close()
        kb = await keyboard_fabric_update.inline_admin_main_menu()

        await message.answer("Вы изменили url пользовательского соглашения", reply_markup=kb)

        await state.clear()
    else:
        await message.answer("Введите текст")


@url_router.callback_query(InlineAdminMenu.filter(F.action == "UrlPolitics"))
async def url_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UrlPoliticEdit.url)
    await callback.message.answer("Введите url")
    await callback.answer()


@url_router.message(UrlPoliticEdit.url)
async def url_edit_user(message: Message, state: FSMContext):
    if message.text:
        await sqlbase_upgrade.connect()
        await sqlbase_upgrade.update_url_politics(message.text)
        await sqlbase_upgrade.close()
        kb = await keyboard_fabric_update.inline_admin_main_menu()
        await message.answer("Вы изменили url политики конфиденциальности", reply_markup=kb)
        await state.clear()
    else:
        await message.answer("Введите текст")


@url_router.callback_query(InlineAdminMenu.filter(F.action == "EditPrice"))
async def url_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UrlPriceEdit.price)
    await callback.message.answer("Введите новую цену")
    await callback.answer()


@url_router.message(UrlPriceEdit.price)
async def url_edit_user(message: Message, state: FSMContext):
    if message.text:
        await sqlbase_upgrade.connect()
        await sqlbase_upgrade.update_url_user(message.text)
        await sqlbase_upgrade.close()
        kb = await keyboard_fabric_update.inline_admin_main_menu()

        await message.answer("Вы изменили цену", reply_markup=kb)
        await state.clear()
    else:
        await message.answer("Введите текст")


@router_for_admin.callback_query(InlineAdminMenu.filter(F.action == "add_faq"))
async def add_faq(callback: CallbackQuery, state: FSMContext):
    await sqlbase_upgrade.connect()
    await state.set_state(AnswerFaq.question)
    await callback.message.answer("Введите вопрос")
    await callback.answer()



@router_for_admin.message(AnswerFaq.question)
async def question(message: Message, state: FSMContext):
    if message.text:

        await state.update_data(question=message.text)
        await state.set_state(AnswerFaq.answer)
        await message.answer("Теперь, введите ответ на вопрос")
    else:
        await message.answer("Введите текст")

@router_for_admin.message(AnswerFaq.answer)
async def answer_faq(message: Message, state: FSMContext):
    if message.text:

        question = await state.get_value("question")
        answer = message.text
        kb = await keyboard_fabric_update.inline_admin_main_menu()
        await sqlbase_upgrade.insert_faq(question, answer)
        await sqlbase_upgrade.close()
        await state.clear()

        await message.answer(f"Вставили вопрос-ответ:\n{question}: {answer}", reply_markup=kb)
    else:
        await message.answer("Введите текст")



@router_for_admin.callback_query(InlineAdminMenu.filter(F.action == "delete_faq"))
async def delete_faq_action(callback: CallbackQuery, state: FSMContext):
    await sqlbase_upgrade.connect()
    faq, ids_faq = await sqlbase_upgrade.select_faq()
    if faq is None:
        await callback.answer("Список вопросов пуст...")
        return
    await state.update_data(ids_faq=ids_faq)
    await state.set_state(DeleteFaq.faq_num)
    await callback.message.answer(f"Вот список вопросов, выберите номер для удаления вопроса-ответа: \n{faq}")
    await callback.answer()

@router_for_admin.message(DeleteFaq.faq_num)
async def delete_faq_num(message: Message, state: FSMContext):
    if message.text:
        ids_faq = await state.get_value("ids_faq")
        try:
            id_faq = int(message.text)
        except ValueError:
            await message.answer("Введите корректный id")
            return

        if id_faq in ids_faq:
            kb = await keyboard_fabric_update.inline_admin_main_menu()

            await sqlbase_upgrade.delete_faq(id_faq)
            await sqlbase_upgrade.close()
            await message.answer("Вы удалили вопрос-ответ", reply_markup=kb)
        else:
            await message.answer("Нет такого номера! Введите корректный номер")

    else:
        await message.answer("Это не текст!")

@router_for_admin.callback_query(InlineAdminMenu.filter(F.action == "truncate_faq"))
async def delete_faq_action(callback: CallbackQuery):
    await sqlbase_upgrade.connect()
    await sqlbase_upgrade.truncate_faq()
    await sqlbase_upgrade.close()
    await callback.answer("FAQ полностью удалён")


