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
                                              description="Получение уведомление о нововышедших подарках",
                                              prices=prices,
                                              provider_token='',
                                              payload="payment_for_the_service",
                                              currency="XTR",
                                              reply_markup=kb
                                              )
    else:
        kb = await pay_fabric_kb.donate_kb()
        await callback.message.edit_text(
            'Вы уже купили услугу, но вы можете пожертвовать звёзды за работу бота,'
            ' если вы хотите их пожертвовать, то нажмите кнопку "Пожертвовать"', reply_markup=kb)

    await callback.answer()


@pay_router.message(F.successful_payment)
async def successful(message: Message):
    transaction_id = message.successful_payment.telegram_payment_charge_id
    amount = message.successful_payment.total_amount
    info = message.successful_payment.invoice_payload
    kb = await pay_fabric_kb.builder_answer_notifications()

    if info == "payment_for_the_service":
        await pay_sqlbase.insert_new_user(str(message.chat.id), transaction_id, amount)

        await message.answer(f"Спасибо, что приобрели нашу услугу\n\n"
                             f"Ваш id транзакции сохраните его, если захотите вернуть звёзды за покупку: "
                             f"<code>{transaction_id}</code>\n"
                             f"Цена: {amount}",
                             reply_markup=kb)
    else:
        await pay_sqlbase.insert_transaction_donat(str(message.chat.id), transaction_id, amount)
        await message.answer(f"Спасибо за поддержку! Пожертвование является добровольным. \n"
                             f"При необходимости вы можете запросить возврат — мы рассмотрим обращение индивидуально.\n\n"
                             f"<code>{transaction_id}</code>",
                             reply_markup=kb)
