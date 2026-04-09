from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from app.keyboards import main_menu
from app.texts import start_text

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(start_text(), reply_markup=main_menu())


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(start_text(), reply_markup=main_menu())


@router.callback_query(lambda c: c.data == "back_main")
async def back_main(callback: CallbackQuery) -> None:
    await callback.message.edit_text(start_text(), reply_markup=main_menu())
    await callback.answer()
