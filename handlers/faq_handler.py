from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.other_operations import OtherOperation
from keyboards.menu_fabric import InlineMainMenu, FabricInline

faq_router = Router()
keyboard_fabric = FabricInline()
sqlbase_faq = OtherOperation()


@faq_router.callback_query(InlineMainMenu.filter(F.action == "faq"))
async def inline_faq(callback: CallbackQuery):
    kb_back = await keyboard_fabric.back_kb()
    await sqlbase_faq.connect()
    all_faq = await sqlbase_faq.select_faq()
    if all_faq is None:
        await callback.answer("Список вопросов пуст...")
    else:
        await callback.message.edit_text(f"{all_faq}", reply_markup=kb_back)

    await sqlbase_faq.close()
    await callback.answer()