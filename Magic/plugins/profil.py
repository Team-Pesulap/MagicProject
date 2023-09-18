import os
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

from config import *
from Magic import*
from Magic.helpers.utils import edit_or_reply
from Magic.helpers.utils import extract_user

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id


flood = {}
pp = "Magic/plugins/resource/pp.jpg"


@ubot.on_message(filters.command(["block"], prefix) & filters.me)
async def block_user_func(client: Client, message: Message):
    mmk = await extract_user(message)
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if not mmk:
        return await message.edit(
            "Berikan User ID/Username atau reply pesan pengguna untuk membuka blokir."
        )
    if mmk == client.me.id:
        return await kontol.edit("Yang Bener Kamu Tuh.")
    await client.block_user(mmk)
    umention = (await client.get_users(mmk)).mention
    await message.edit(f"**Berhasil Memblokir** {umention}")


@ubot.on_message(filters.command(["unblock"], prefix) & filters.me)
async def unblock_user_func(client: Client, message: Message):
    mmk = await extract_user(message)
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if not mmk:
        return await message.edit(
            "Berikan User ID/Username atau reply pesan pengguna untuk membuka blokir."
        )
    if mmk == client.me.id:
        return await kontol.edit("Yang Bener Kamu Tuh.")
    await client.unblock_user(mmk)
    umention = (await client.get_users(mmk)).mention
    await message.edit(f"**Berhasil Membuka Blokir** {umention}")


@ubot.on_message(filters.command(["setname"], prefix) & filters.me)
async def setname(client: Client, message: Message):
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if len(message.command) == 1:
        return await kontol.edit(
            "Berikan teks untuk ditetapkan sebagai nama telegram anda."
        )
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await kontol.edit(f"**Berhasil Mengubah Nama Telegram anda Menjadi** `{name}`")
        except Exception as e:
            await kontol.edit(f"**ERROR:** `{e}`")
    else:
        return await kontol.edit(
            "Berikan teks untuk ditetapkan sebagai nama telegram anda."
        )


@ubot.on_message(filters.command(["setbio"], prefix) & filters.me)
async def set_bio(client: Client, message: Message):
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if len(message.command) == 1:
        return await kontol.edit("Berikan teks untuk ditetapkan sebagai bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await kontol.edit(f"**Berhasil Mengubah BIO anda menjadi** `{bio}`")
        except Exception as e:
            await kontol.edit(f"**ERROR:** `{e}`")
    else:
        return await kontol.edit("Berikan teks untuk ditetapkan sebagai bio.")


@ubot.on_message(filters.me & filters.command(["setpp"], prefix))
async def set_pp(client: Client, message: Message):
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        await client.download_media(message=replied, file_name=pp)
        await client.set_pp(pp)
        if os.path.exists(pp):
            os.remove(pp)
        await message.edit("**Foto Profil anda Berhasil Diubah.**")
    else:
        await message.edit(
            "`Balas ke foto apa pun untuk dipasang sebagai foto profile`"
        )
        await sleep(3)
        await message.delete()


@ubot.on_message(filters.me & filters.command(["vpp"], prefix))
async def view_pp(client: Client, message: Message):
    mmk = await extract_user(message)
    if mmk:
        anuan = await client.get_users(mmk)
    else:
        anuan = await client.get_me()
    if not anuan.photo:
        await message.edit("Foto profil tidak ditemukan!")
        return
    await client.download_media(anuan.photo.big_file_id, file_name=pp)
    await client.send_photo(
        message.chat.id, pp, reply_to_message_id=ReplyCheck(message)
    )
    await message.delete()
    if os.path.exists(pp):
        os.remove(pp)
