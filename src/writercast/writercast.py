from __future__ import annotations

import time

from discordrp import Presence
from secretbox import SecretBox

APP_ID = SecretBox(auto_load=True).get("WRITERCAST_CAST_ID", "")


with Presence(APP_ID) as presence:
    print("Connected")
    presence.set(
        {
            "state": "Developing",
            "details": "WriterCast",
            "timestamps": {"start": int(time.time())},
        }
    )
    print("Presence updated")

    while True:
        time.sleep(15)
