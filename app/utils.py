from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import settings


def now_local() -> datetime:
    return datetime.now(ZoneInfo(settings.event_timezone))


def today_str() -> str:
    return now_local().strftime("%Y-%m-%d")


def is_valid_time_string(value: str) -> bool:
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False
