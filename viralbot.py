import os
import re
import urllib.parse
import asyncio
import json
import requests
from pyrogram import Client, filters
from dotenv import load_dotenv
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from quart import Quart
from pyrogram import enums

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
 # Your EarnKaro API token

# Initialize Pyrogram bot
bot = Client("promo_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize Quart app
app = Quart(__name__)


SOURCE_CHANNEL_ID= -1002482808575
SOURCE_MESSAGE_ID= 3
# Health check route (for hosting platforms)
@app.route("/")
async def home():
    return {"status": "running", "message": "promo Bot is alive!"}

PostingChannel=[-1002406969774,-1003440216101,-1002993106861]

Promo = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Click here to See more 🤫", url="https://t.me/addlist/gu7nU3yNklJhMTc9")]
     ])
def extract_diskwala_links(text: str) -> list[str]:
    return re.findall(
        r"https?://(?:www\.)?diskwala\.com/\S+",
        text
    )

source_channel_id=[-1002803694251]

@bot.on_message(filters.chat(PostingChannel))
async def forward_message(client, message):

    text = message.caption if message.caption else message.text or ""
    if not text:
        return

    links = extract_diskwala_links(text)
    # print(links)
    if not links:
        return  # diskwala link nahi mila → ignore

    links_block = "\n\n➡️".join(links)
    new_text = f"""🎬 ** 🔗🔗🔗 :👇**
    {links_block}

    🤔 **How to Open Links 👇👇 see tutorial Video 👇🏻🤗**
    https://t.me/diskhow/3

    𝐉𝐨𝐢𝐧 this 𝐁𝐚𝐜𝐤𝐮𝐩 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 💾 for All New trending Videos 👇🏻👇🏻
    https://t.me/+HQmvZytWmeI2YWM1
    """

    print(f'Found a Diskwala link')

    try:
        # run blocking ekconvert in a thread pool to avoid blocking the event loop
        # converted = await asyncio.get_event_loop().run_in_executor(None, ekconvert, text)

        # Try editing and log any exception
        if message.photo:
            try:
                await client.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    caption=new_text,
                    reply_markup=Promo
                )
                print("Edited caption immediately:", message.id)
            except Exception as e:
                print("Edit caption failed:", repr(e))
        elif message.text:
            try:
                await client.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    text=new_text,
                    disable_web_page_preview=True,

                )
                print("Edited text immediately:", message.id)
            except Exception as e:
                print("Edit text failed:", repr(e))
        elif message.media:
            try:
                await client.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    caption=new_text
                )
                print("Edited caption immediately:", message.id)
            except Exception as e:
                print("Edit caption failed:", repr(e))

    except Exception as e:
        print("Conversion failed:", repr(e))





@bot.on_message(filters.private  and filters.incoming and ~filters.command("start") and ~filters.regex('start'))
async def send_links(client, message):
    text = message.caption if message.caption else message.text
    if 'Livegram' in text or 'You cannot forward someone' in text:
        await message.delete()
        return

@bot.on_message(filters.command("start") or filters.regex('start'))
async def start_cmd(client, message):
    # print(message.chat.type)
    # if message.chat.type != ChatType.PRIVATE:
    #     return
    # text = message.caption if message.caption else message.text
    # print(text)
    # if 'Livegram' in text or 'You cannot forward someone' in text:
    #     await message.delete()
    #     # return None

    await bot.forward_messages(
        chat_id=message.chat.id,
        from_chat_id=SOURCE_CHANNEL_ID,
        message_ids=SOURCE_MESSAGE_ID,

    )

@app.before_serving
async def before_serving():
    await bot.start()


@app.after_serving
async def after_serving():
    await bot.stop()
# Run bot + quart together
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(app.run_task(host='0.0.0.0', port=8080))
    loop.run_forever()