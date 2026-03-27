from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from bot.keyboards import main_menu_kb

router = Router()

HEADER = (
    "╔══════════════════════════════╗\n"
    "║      AMNEZIA VPN MANAGER     ║\n"
    "╚══════════════════════════════╝"
)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(HEADER, reply_markup=main_menu_kb())

@router.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(HEADER, reply_markup=main_menu_kb())