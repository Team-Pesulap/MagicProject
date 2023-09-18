import os
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

from config import *
from Magic import *
from Magic.helpers.utils import edit_or_reply
from Magic.helpers.utils import extract_user, extract_user_and_reason

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id


flood = {}
pp = "Magic/plugins/resource/pp.jpg"


@ubot.on_message(filters.command("block", prefix) & filters.me)
async def block_user_func(client: Client, message: Message):
    mmk = await extract_user(message)
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if not mmk:
        return await message.edit(
            "Provide User ID/Username or reply to user message to block."
        )
    if mmk == client.me.id:
        return await kontol.edit("Wait")
    await client.block_user(mmk)
    umention = (await client.get_users(mmk)).mention
    await message.edit(f"**Successfully Blocked User** {umention}")


@ubot.on_message(filters.command("unblock", prefix) & filters.me)
async def unblock_user_func(client: Client, message: Message):
    mmk = await extract_user(message)
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if not mmk:
        return await message.edit(
            "Provide User ID/Username or reply to user message to unblock."
        )
    if mmk == client.me.id:
        return await kontol.edit("Wait")
    await client.unblock_user(mmk)
    umention = (await client.get_users(mmk)).mention
    await message.edit(f"**Successfully Unblocked** {umention}")


@ubot.on_message(filters.command("setname", prefix) & filters.me)
async def setname(client: Client, message: Message):
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if len(message.command) == 1:
        return await kontol.edit(
            "Provide text to set as your telegram name."
        )
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await kontol.edit(f"**Successfully changed your Telegram name to** `{name}`")
        except Exception as e:
            await kontol.edit(f"**ERROR:** `{e}`")
    else:
        return await kontol.edit(
            "Provide text to set as your telegram name."
        )


@ubot.on_message(filters.command("setbio", prefix) & filters.me)
async def set_bio(client: Client, message: Message):
    kontol = await edit_or_reply(message, "`Processing . . .`")
    if len(message.command) == 1:
        return await kontol.edit("Provide text to set as bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await kontol.edit(f"**Successfully Changed your BIO to** `{bio}`")
        except Exception as e:
            await kontol.edit(f"**ERROR:** `{e}`")
    else:
        return await kontol.edit("Provide text to set as bio.")


@ubot.on_message(filters.me & filters.command("setpp", prefix))
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
        await message.edit("**Your profile photo has been successfully changed.**")
    else:
        await message.edit(
            "`Reply to any photo to set as a profile photo`"
        )
        await sleep(3)
        await message.delete()


@ubot.on_message(filters.me & filters.command("vpp", prefix))
async def view_pp(client: Client, message: Message):
    mmk = await extract_user(message)
    if mmk:
        anuan = await client.get_users(mmk)
    else:
        anuan = await client.get_me()
    if not anuan.photo:
        await message.edit("Profile photo not found!")
        return
    await client.download_media(anuan.photo.big_file_id, file_name=pp)
    await client.send_photo(
        message.chat.id, pp, reply_to_message_id=ReplyCheck(message)
    )
    await message.delete()
    if os.path.exists(pp):
        os.remove(pp)
