import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    bot_token: str
    admin_ids: list[int]
    db_path: str
    event_timezone: str
    event_title: str
    default_times: list[str]


def parse_admin_ids(raw_value: str) -> list[int]:
    if not raw_value.strip():
        return []

    result = []
    for item in raw_value.split(","):
        item = item.strip()
        if item:
            result.append(int(item))
    return result


def parse_default_times(raw_value: str) -> list[str]:
    if not raw_value.strip():
        return ["18:00", "18:30", "19:00", "19:30", "20:00"]

    result = []
    for item in raw_value.split(","):
        item = item.strip()
        if item:
            result.append(item)
    return result


settings = Settings(
    bot_token=os.getenv("BOT_TOKEN", "").strip(),
    admin_ids=parse_admin_ids(os.getenv("ADMIN_IDS", "")),
    db_path=os.getenv("DB_PATH", "bot.db").strip(),
    event_timezone=os.getenv("EVENT_TIMEZONE", "Europe/Amsterdam").strip(),
    event_title=os.getenv("EVENT_TITLE", "Сегодняшнее мероприятие").strip(),
    default_times=parse_default_times(
        os.getenv("DEFAULT_TIMES", "18:00,18:30,19:00,19:30,20:00")
    ),
)