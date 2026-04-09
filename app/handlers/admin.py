from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import settings
from app.database import get_today_coming_list

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("list"))
async def list_today(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администратору.")
        return

    rows = get_today_coming_list()

    if not rows:
        await message.answer("На сегодня пока никто не записался.")
        return

    lines = ["Список на сегодня:\n"]

    for idx, row in enumerate(rows, start=1):
        full_name = (row["full_name"] or "").strip()
        username = (row["username"] or "").strip()
        arrival_time = (row["arrival_time"] or "").strip()

        if full_name and username:
            name = f"{full_name} (@{username})"
        elif full_name:
            name = full_name
        elif username:
            name = f"@{username}"
        else:
            name = f"id:{row['user_id']}"

        time_text = arrival_time if arrival_time else "свое время не указано"
        lines.append(f"{idx}. {name} — {time_text}")

    await message.answer("\n".join(lines))