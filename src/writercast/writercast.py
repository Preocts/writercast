from __future__ import annotations

import time
from datetime import datetime

from discordrp import Presence
from secretbox import SecretBox

APP_ID = SecretBox(auto_load=True).get("WRITERCAST_CAST_ID", "")


def timestamp_bookends() -> tuple[int, int]:
    """Return the start of today and the end of today as timestamps."""
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(hour=23, minute=59, second=59, microsecond=999999)
    return int(start.timestamp()), int(end.timestamp())


def main() -> int:
    """Run the main loop."""
    try:
        presence = Presence(APP_ID)
        print("Starting WriterCast...")
        day = 0

        while "The words flow from the fountain of inspiration":
            if datetime.now().day != day:
                day = datetime.now().day
                build_presence(day, presence)
                print(f"Day {day} of 30")

            time.sleep(15)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        presence.close()

    return 0


def build_presence(day: int, presence: Presence) -> None:
    """Build the presence."""
    start, end = timestamp_bookends()
    presence.clear()
    presence.set(
        {
            "state": f"Day {day} of 30",
            "details": "NaNoWriMo 2023",
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
    )


if __name__ == "__main__":
    raise SystemExit(main())
