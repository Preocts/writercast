from __future__ import annotations

import dataclasses
import datetime
import sqlite3
import time
from typing import Any

from discordrp import Presence
from secretbox import SecretBox

APP_ID = SecretBox(auto_load=True).get("WRITERCAST_CAST_ID", "")
REFRESH_RATE = 15  # seconds
WORD_GOAL = 50_000
DATABASE_PATH = "writercast.db"
MAX_RETRIES = 5


def timestamp_bookends() -> tuple[int, int]:
    """Return the start of today and the end of today as timestamps."""
    start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(hour=23, minute=59, second=59, microsecond=999999)
    return int(start.timestamp()), int(end.timestamp())


def get_word_count() -> int:
    try:
        with open("wordcount.txt") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0


def main() -> int:
    """Run the main loop."""
    retry_count = 0
    while "All the things that she said, running through my head":
        try:
            presence = Presence(APP_ID)
            print("Starting WriterCast...")
            day = 0
            start = 0
            end = 0

            while "The words flow from the fountain of inspiration":
                if datetime.datetime.now().day != day:
                    day = datetime.datetime.now().day
                    start, end = timestamp_bookends()
                    print(f"Day {day} of 30")

                word_count = get_word_count()

                payload = build_payload(day, start, end, word_count, WORD_GOAL)
                presence.clear()
                presence.set(payload)

                time.sleep(REFRESH_RATE)
                retry_count = 0

        except OSError:
            print("Could not connect to Discord. Is Discord running?")
            time.sleep(REFRESH_RATE)
            retry_count += 1
            if retry_count > MAX_RETRIES:
                print("Too many retries. Exiting...")
                return 1

        except KeyboardInterrupt:
            print("Exiting...")
            return 0

        finally:
            presence.close()

    return 0


def build_payload(
    day: int,
    start: int,
    end: int,
    word_count: int,
    word_goal: int,
) -> dict[str, Any]:
    """Build the presence."""
    return {
        "state": f"Day {day} of 30",
        "details": f"NaNoWriMo ({word_count:,} / {word_goal:,} words)",
        "timestamps": {
            "start": start,
            "end": end,
        },
        "assets": {
            "large_image": "nanowrimo_logo",
            "large_text": "NaNoWriMo 2023",
        },
        "buttons": [
            {
                "label": "NaNoWriMo",
                "url": "https://nanowrimo.org",
            },
        ],
    }


@dataclasses.dataclass(frozen=True)
class DBRow:
    timestamp: int
    wordcount: int


def _create_database_table(database: sqlite3.Connection) -> None:
    """Create the database table."""
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS wordcount (
            timestamp INTEGER PRIMARY KEY,
            wordcount INTEGER NOT NULL
        )
        """
    )


def _add_wordcount(database: sqlite3.Connection, wordcount: int) -> None:
    """Add a wordcount to the database."""
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    cursor = database.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO wordcount (timestamp, wordcount)
            VALUES (?, ?)
            """,
            (int(now.timestamp()), wordcount),
        )

    finally:
        cursor.close()


def _get_wordcount(database: sqlite3.Connection) -> list[DBRow]:
    """Get the wordcount from the database."""
    cursor = database.cursor()
    try:
        cursor.execute(
            """
            SELECT timestamp, wordcount
            FROM wordcount
            ORDER BY timestamp DESC
            """
        )
        return [DBRow(*row) for row in cursor.fetchall()]

    finally:
        cursor.close()


if __name__ == "__main__":
    raise SystemExit(main())
