from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext

router_gift = Router(name="gift_router")

@router_gift.message(Command("replenishment"))
async def replenishment_handler(message: Message, state: FSMContext):
    awa


