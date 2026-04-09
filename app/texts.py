from app.config import settings


def start_text() -> str:
    return (
        f"<b>{settings.event_title}</b>\n\n"
        "Отметься на сегодня и выбери примерное время прихода."
    )


CHOOSE_TIME = "Во сколько примерно придешь?"
CUSTOM_TIME_REQUEST = (
    "Отправь время в формате <b>ЧЧ:ММ</b>.\n"
    "Например: <code>18:45</code>"
)
NOT_COMING_SAVED = "Ок, отметил, что сегодня тебя не будет."
UNKNOWN_TIME = "не выбрано"


def status_text(status: str | None, arrival_time: str | None) -> str:
    if not status:
        return "Ты пока не отмечался на сегодня."
    if status == "coming":
        return (
            "<b>Твой статус:</b> приду\n"
            f"<b>Время:</b> {arrival_time or UNKNOWN_TIME}"
        )
    return "<b>Твой статус:</b> не приду"


def coming_saved_text(arrival_time: str) -> str:
    return (
        "Готово. Записал, что ты придешь сегодня.\n"
        f"<b>Время:</b> {arrival_time}"
    )


INVALID_TIME = "Не получилось распознать время. Отправь его в формате <b>ЧЧ:ММ</b>, например <code>19:15</code>."
NO_ONE_COMING = "На сегодня пока никто не отметил, что придет."
