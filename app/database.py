import sqlite3
from contextlib import closing
from typing import Any

from app.config import settings
from app.utils import today_str


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT,
    full_name TEXT,
    status TEXT NOT NULL,
    arrival_time TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_date, user_id)
)
"""


CREATE_STATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS user_states (
    user_id INTEGER PRIMARY KEY,
    state TEXT NOT NULL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn



def init_db() -> None:
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        cur.execute(CREATE_STATE_TABLE_SQL)
        conn.commit()



def save_registration(
    *,
    user_id: int,
    username: str | None,
    full_name: str,
    status: str,
    arrival_time: str | None,
    event_date: str | None = None,
) -> None:
    event_date = event_date or today_str()
    with closing(get_connection()) as conn:
        conn.execute(
            """
            INSERT INTO registrations (event_date, user_id, username, full_name, status, arrival_time, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(event_date, user_id) DO UPDATE SET
                username=excluded.username,
                full_name=excluded.full_name,
                status=excluded.status,
                arrival_time=excluded.arrival_time,
                updated_at=CURRENT_TIMESTAMP
            """,
            (event_date, user_id, username, full_name, status, arrival_time),
        )
        conn.commit()



def get_user_registration(user_id: int, event_date: str | None = None) -> sqlite3.Row | None:
    event_date = event_date or today_str()
    with closing(get_connection()) as conn:
        row = conn.execute(
            """
            SELECT *
            FROM registrations
            WHERE event_date = ? AND user_id = ?
            """,
            (event_date, user_id),
        ).fetchone()
        return row



def get_today_coming_list(event_date: str | None = None) -> list[sqlite3.Row]:
    event_date = event_date or today_str()
    with closing(get_connection()) as conn:
        rows = conn.execute(
            """
            SELECT full_name, username, arrival_time
            FROM registrations
            WHERE event_date = ? AND status = 'coming'
            ORDER BY arrival_time IS NULL, arrival_time, full_name
            """,
            (event_date,),
        ).fetchall()
        return rows



def get_today_stats(event_date: str | None = None) -> dict[str, Any]:
    event_date = event_date or today_str()
    with closing(get_connection()) as conn:
        totals = conn.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'coming' THEN 1 ELSE 0 END) AS coming_count,
                SUM(CASE WHEN status = 'not_coming' THEN 1 ELSE 0 END) AS not_coming_count
            FROM registrations
            WHERE event_date = ?
            """,
            (event_date,),
        ).fetchone()

        by_time = conn.execute(
            """
            SELECT COALESCE(arrival_time, 'не выбрано') AS arrival_time, COUNT(*) AS cnt
            FROM registrations
            WHERE event_date = ? AND status = 'coming'
            GROUP BY COALESCE(arrival_time, 'не выбрано')
            ORDER BY arrival_time
            """,
            (event_date,),
        ).fetchall()

    return {
        "total": totals["total"] or 0,
        "coming_count": totals["coming_count"] or 0,
        "not_coming_count": totals["not_coming_count"] or 0,
        "by_time": by_time,
    }



def set_user_state(user_id: int, state: str) -> None:
    with closing(get_connection()) as conn:
        conn.execute(
            """
            INSERT INTO user_states (user_id, state, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                state=excluded.state,
                updated_at=CURRENT_TIMESTAMP
            """,
            (user_id, state),
        )
        conn.commit()



def get_user_state(user_id: int) -> str | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT state FROM user_states WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return row["state"] if row else None



def clear_user_state(user_id: int) -> None:
    with closing(get_connection()) as conn:
        conn.execute("DELETE FROM user_states WHERE user_id = ?", (user_id,))
        conn.commit()
from app.utils import today_str
from app.config import settings
import sqlite3


def get_connection():
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_today_coming_list():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id, username, full_name, arrival_time
        FROM registrations
        WHERE event_date = ? AND status = 'coming'
        ORDER BY
            CASE WHEN arrival_time IS NULL OR arrival_time = '' THEN 1 ELSE 0 END,
            arrival_time ASC,
            full_name ASC
        """,
        (today_str(),)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows