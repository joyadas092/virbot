"""
One-time migration: tag all pre-existing user docs (from before the multi-bot
change) with bot_keys/bots.<bot_key> so /broadcast on bot 1 still reaches them.

Run once, after setting BOT1_USERNAME below to bot 1's real @username
(the one all 7k existing users originally interacted with).

    python migrate_backfill_bot_keys.py
"""
import asyncio
import os
import re
from datetime import datetime, timezone

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "").strip()
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "teradl").strip()

# Bot 1's username (no leading @) - the bot these 7k users originally used.
BOT1_USERNAME = os.getenv("BOT_USERNAME", "").strip()


def sanitize_bot_key(raw: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", (raw or "").lower()) or "bot_1"


async def main():
    if not MONGO_URI:
        raise SystemExit("MONGO_URI not set")
    if not BOT1_USERNAME:
        raise SystemExit("Set BOT_USERNAME in .env (or edit BOT1_USERNAME above) to bot 1's real username")

    bot_key = sanitize_bot_key(BOT1_USERNAME)
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    users_col = db["users"]

    now = datetime.now(timezone.utc)
    result = await users_col.update_many(
        {"bot_keys": {"$exists": False}},
        {
            "$set": {
                f"bots.{bot_key}.last_seen_at": now,
                f"bots.{bot_key}.bot_username": bot_key,
            },
            "$addToSet": {"bot_keys": bot_key},
        },
    )
    print(f"Backfilled bot_key='{bot_key}' onto {result.modified_count} existing user docs.")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
