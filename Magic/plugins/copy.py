from Magic import *
from pyrogram import filters
from pyrogram.types import Message
import os
from config import *

@ubot.on_message(filters.command("copy", prefix) & filters.me)
async def copy_command(client, message: Message):
    try:
        await message.edit("Processing...")
        link = message.text.split(" ", 1)[1]

        chat_id = int("-100" + link.split("/")[-1]) if "t.me/c/" in link else link.split("/")[-1]
        msg_id = int(link.split("/")[-1])
        bkp = await client.get_messages(chat_id, msg_id)
        laras = bkp.caption if bkp.caption else None

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
        print(f"ERROR: {e}")
