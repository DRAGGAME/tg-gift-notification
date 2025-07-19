from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, Message
from aiogram.types import PreCheckoutQuery

from database.other_operations import OtherOperation
from keyboards.menu_fabric import InlineMainMenu, FabricInline

pay_router = Router()
pay_sqlbase = OtherOperation()
pay_fabric_kb = FabricInline()


@pay_router.callback_query(InlineMainMenu.filter(F.action == "pay"))
async def pay_button_false(callback: CallbackQuery):
    await pay_sqlbase.connect()
    chat_id = callback.message.chat.id

    user_pay = await pay_sqlbase.select_user_for_pay(str(chat_id))
    if user_pay:

        kb, price = await pay_fabric_kb.pay_kb(pay_sqlbase)
        prices = [LabeledPrice(label="XTR", amount=price)]
        await callback.message.answer_invoice(title='Получать уведомления о подарках',
                                              description="Оплата счёта",
                                              prices=prices,
                                              provider_token='',
                                              payload="payment_for_the_service",
                                              currency="XTR",
                                              reply_markup=kb
                                              )
    else:
        await callback.message.edit_text('Вы уже купили товар')
    await callback.answer()


@pay_router.pre_checkout_query()
async def pre_checkout_handler(message: Message, pre_checkout_query: PreCheckoutQuery):
    await message.delete()
    await pre_checkout_query.answer(ok=True)

