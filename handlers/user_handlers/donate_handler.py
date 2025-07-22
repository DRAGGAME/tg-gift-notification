import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, LabeledPrice

from keyboards.menu_fabric import InlineMainMenu, FabricInline

donate_router = Router()
donate_fabric_kb = FabricInline()

class Donate(StatesGroup):
    amount = State()

@donate_router.callback_query(InlineMainMenu.filter(F.action=="donate"))
async def donate_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Donate.amount)
    kb = await donate_fabric_kb.back_kb()
    await callback.message.edit_text("Введите, сколько вы хотите пожертвовать", reply_markup=kb)

@donate_router.message(Donate.amount)
async def donate_amount_message(message: Message, state: FSMContext):
    if message.text:
        try:
            amount = int(message.text)
            if amount > 0:
                kb, amount = await donate_fabric_kb.pay_kb(sqlbase=None, price=amount)
                prices = [LabeledPrice(label="XTR", amount=amount)]
                await message.answer_invoice(title='Добровольное пожертвование',
                                                      description="Пожертвование администратору бота",
                                                      prices=prices,
                                                      provider_token='',
                                                      payload="donate",
                                                      currency="XTR",
                                                      reply_markup=kb
                                                      )
                await state.clear()
                return
            else:
                await message.answer("Нельзя пожертвовать меньше 1 звезды")
        except ValueError:
            await message.answer("Вы ввели не целое число")
    else:
        await message.reply("Введите текст")
    await asyncio.sleep(20)
    await message.delete()

