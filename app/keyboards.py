from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings


def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Приду", callback_data="coming")
    kb.button(text="❌ Не приду", callback_data="not_coming")
    kb.button(text="🕒 Изменить время", callback_data="change_time")
    kb.button(text="ℹ️ Мой статус", callback_data="my_status")
    kb.adjust(1)
    return kb.as_markup()


def time_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for t in settings.default_times:
        kb.button(text=t, callback_data=f"time:{t}")
    kb.button(text="✍️ Ввести свое время", callback_data="custom_time")
    kb.button(text="⬅️ Назад", callback_data="back_main")
    kb.adjust(2, 2, 1)
    return kb.as_markup()
