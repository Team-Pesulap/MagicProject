from Magic import *
from pyrogram import filters
from pyrogram.types import Message
import os
from config import *

@ubot.on_message(filters.command("copy", prefix) & filters.me)
async def nyolongnih(client, message):
    try:
        await message.reply("Processing...")
        link = message.text.split(" ", 1)[1]
        msg_id = int(link.split("/")[-1])
        
        if "t.me/c/" in link:
            try:
                chat = int("-100" + str(link.split("/")[-2]))
                bkp = await client.get_messages(chat, msg_id)
            except RPCError:
                await message.edit("Looks like an error occurred")
        else:
            try:
                chat = str(link.split("/")[-2])
                bkp = await client.get_messages(chat, msg_id)
            except RPCError:
                await message.edit("Looks like an error occurred")

        laras = bkp.caption or None

        media_types = {
            "text": bkp.text,
            "photo": bkp.photo,
            "video": bkp.video,
            "audio": bkp.audio,
            "voice": bkp.voice,
            "document": bkp.document
        }

        for media_type, media_data in media_types.items():
            if media_data:
                media = await client.download_media(bkp)
                send_func = getattr(client, f"send_{media_type}")
                await send_func(message.chat.id, media, caption=laras)
                os.remove(media)
                break
        else:
            await message.edit("Failed to download the content...")

        await message.delete()

    except Exception as e:
        await message.reply(f"ERROR: {e}")
