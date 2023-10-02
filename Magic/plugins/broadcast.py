import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors.exceptions.flood_420 import FloodWait

from Magic import *
from Magic.helpers import get_arg
from config import *


def extract_argument(message: Message):
    pesan = message.text
    pesan = pesan.replace(" ", "", 1) if pesan[1] == " " else pesan
    split = pesan[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


async def get_target(client, query):
    chats = []
    chat_types = {
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE],
    }
    async for dialog in client.get_dialogs():
        if dialog.chat.type in chat_types[query]:
            chats.append(dialog.chat.id)
    return chats


@ubot.on_message(filters.command("gcast", prefix) & filters.me)
async def global_broadcast(client: Client, message: Message):
    if message.reply_to_message or extract_argument(message):
        msg = message.reply_to_message
        ea = extract_argument(message)
        amg = await message.reply("`Globally Broadcasting...`")
    else:
        return await message.reply("`Please reply or leave a message.`")
    berhasil = 0
    gagal = 0
    target = await get_target(client, "group")
    cekbl = MDB.get_key("BLACKLIST_GCAST") or []
    cekbl.append(-)
    MDB.set_key("BLACKLIST_GCAST", cekbl)

    for gc_id in target:
        if gc_id not in cekbl and gc_id not in BLACKLIST_CHAT:
            try:
                if message.reply_to_message:
                    await msg.copy(gc_id)
                else:
                    await client.send_message(gc_id, ea)
                berhasil += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                if message.reply_to_message:
                    await msg.copy(gc_id)
                else:
                    await client.send_message(gc_id, ea)
                berhasil += 1
            except Exception:
                pass

    await amg.edit(f"**Successfully Sent Message To `{berhasil}` Groups chat. Failed: `{gagal}`**.")


@ubot.on_message(filters.command(["addbl", "delbl"], prefix) & filters.me)
async def lock_bl(message, tipe):
    tt = get_arg(message)
    if len(tt) > 2:
        return await message.reply("**Gunakan Format:**\n `delbl` or `addbl`")
    gc = None
    gc = int(tt[1]) if len(tt) == 2 else message.chat_id
    if tt.lower() == "addbl":
        add_bl(gc)
        await message.reply(f"**Grup berhasil ditambahkan ke Blacklist Gcast Ya Kontol Kuda**\n`{gc}`")
    elif tt.lower() == "delbl":
        un_bl(gc)
        await message.reply(f"**Grup berhasil dihapus dari Blacklist Gcast Ya Memek Busuk**\n`{gc}`")