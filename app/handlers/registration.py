from aiogram import Router
from aiogram.types import CallbackQuery, Message

from app.database import (
    clear_user_state,
    get_user_registration,
    get_user_state,
    save_registration,
    set_user_state,
)
from app.keyboards import main_menu, time_menu
from app.texts import (
    CHOOSE_TIME,
    CUSTOM_TIME_REQUEST,
    INVALID_TIME,
    NOT_COMING_SAVED,
    coming_saved_text,
    start_text,
    status_text,
)
from app.utils import is_valid_time_string

router = Router()



def _full_name(user) -> str:
    return " ".join(part for part in [user.first_name, user.last_name] if part).strip() or "Без имени"


@router.callback_query(lambda c: c.data == "coming")
async def choose_coming(callback: CallbackQuery) -> None:
    save_registration(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=_full_name(callback.from_user),
        status="coming",
        arrival_time=None,
    )
    clear_user_state(callback.from_user.id)
    await callback.message.edit_text(CHOOSE_TIME, reply_markup=time_menu())
    await callback.answer()


@router.callback_query(lambda c: c.data == "change_time")
async def change_time(callback: CallbackQuery) -> None:
    row = get_user_registration(callback.from_user.id)
    if not row or row["status"] != "coming":
        await callback.message.edit_text(
            "Сначала отметься, что придешь.",
            reply_markup=main_menu(),
        )
    else:
        await callback.message.edit_text(CHOOSE_TIME, reply_markup=time_menu())
    await callback.answer()


@router.callback_query(lambda c: c.data == "not_coming")
async def not_coming(callback: CallbackQuery) -> None:
    save_registration(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=_full_name(callback.from_user),
        status="not_coming",
        arrival_time=None,
    )
    clear_user_state(callback.from_user.id)
    await callback.message.edit_text(NOT_COMING_SAVED, reply_markup=main_menu())
    await callback.answer()


@router.callback_query(lambda c: c.data == "my_status")
async def my_status(callback: CallbackQuery) -> None:
    row = get_user_registration(callback.from_user.id)
    text = status_text(row["status"], row["arrival_time"]) if row else status_text(None, None)
    await callback.message.edit_text(text, reply_markup=main_menu())
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("time:"))
async def choose_time(callback: CallbackQuery) -> None:
    arrival_time = callback.data.split(":", 1)[1]
    save_registration(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=_full_name(callback.from_user),
        status="coming",
        arrival_time=arrival_time,
    )
    clear_user_state(callback.from_user.id)
    await callback.message.edit_text(coming_saved_text(arrival_time), reply_markup=main_menu())
    await callback.answer()


@router.callback_query(lambda c: c.data == "custom_time")
async def custom_time(callback: CallbackQuery) -> None:
    set_user_state(callback.from_user.id, "waiting_custom_time")
    await callback.message.edit_text(CUSTOM_TIME_REQUEST, reply_markup=main_menu())
    await callback.answer()


@router.message()
async def handle_custom_time(message: Message) -> None:
    state = get_user_state(message.from_user.id)
    if state != "waiting_custom_time":
        return

    raw_time = (message.text or "").strip()
    if not is_valid_time_string(raw_time):
        await message.answer(INVALID_TIME)
        return

    save_registration(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=_full_name(message.from_user),
        status="coming",
        arrival_time=raw_time,
    )
    clear_user_state(message.from_user.id)
    await message.answer(coming_saved_text(raw_time), reply_markup=main_menu())
    await message.answer(start_text(), reply_markup=main_menu())
