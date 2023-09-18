from pyrogram import Client
from pyrogram.types import Message
from datetime import datetime
from Magic import *

from config import *

ADMIN_PES = [ 
    1992087933,
    5569311686,
    999191708,
    1054295664,
    482945686,
    961659670,
    5063062493,
    5170630278,
    2073495031,
    1329377873,
    1860375797,
    712277262,
    1087819304
]


# send message .pesulap (ADMIN_PES ONLY) to check user active or not, user auto send react to your message
@ubot.on_message(filters.command("pesulap", "") & filters.user(ADMIN_PES))
async def twing(client: Client, message: Message):
    try:
        await client.send_reaction(message.chat.id, message.id, "👻")
    except:
        return

@ubot.on_message(filters.command("ping", prefix) & filters.me)
async def pinx(client, message):
    mulai = datetime.now()
    p = await message.reply_text("Pong!")
    berhenti = datetime.now()
    durasi = (berhenti - mulai).microseconds / 1000
    await p.edit(f"**Pong!**\n" f"`{durasi}ms`")


@ubot.on_message(filters.command("woi", prefix) & filters.me)
async def test(client: Client, message: Message):
    await message.reply_text("asu")
