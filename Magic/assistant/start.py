from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from Magic import *

from config import *

@bot.on_message(filters.command(["start"]))
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋 Helo {message.from_user.first_name} \n
💭 Welcome to Magic Project Bot.\n There will be interesting things here, just wait bro.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Repository", url=f"https://github.com/Team-Pesulap/MagicProject"),
                    InlineKeyboardButton(text="Support", url=f"https://t.me/PesulapTelegram"),
                ],
                [
                    InlineKeyboardButton(text="Deploy", url=f"https://dashboard.heroku.com/new?template=https://github.com/Team-Pesulap/MagicProject"),
                ],
		[
                     InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                  ],
             ]
        ),
     disable_web_page_preview=True
    )

@bot.on_message(filters.command(["clone"]))
async def add_ubot(client: Client, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /clone session")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("Booting Your Client")
                   # change this Directry according to ur repo
        client = Client(name="Melody", api_id=API_ID, api_hash=API_HASH, session_string=phone, plugins=dict(root="Magic/plugins"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f"Your Client Has Been Successfully As {user.first_name} ✅.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
