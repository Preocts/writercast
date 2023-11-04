from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from discordrp import Presence
from secretbox import SecretBox

APP_ID = SecretBox(auto_load=True).get("WRITERCAST_CAST_ID", "")
REFRESH_RATE = 15  # seconds
WORD_GOAL = 50_000


def timestamp_bookends() -> tuple[int, int]:
    """Return the start of today and the end of today as timestamps."""
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
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
    try:
        presence = Presence(APP_ID)
        print("Starting WriterCast...")
        day = 0
        start = 0
        end = 0

        while "The words flow from the fountain of inspiration":
            if datetime.now().day != day:
                presence.clear()
                day = datetime.now().day
                start, end = timestamp_bookends()
                print(f"Day {day} of 30")

            word_count = get_word_count()

            payload = build_payload(day, start, end, word_count, WORD_GOAL)
            presence.set(payload)

            time.sleep(REFRESH_RATE)

    except KeyboardInterrupt:
        print("Exiting...")

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


if __name__ == "__main__":
    raise SystemExit(main())
