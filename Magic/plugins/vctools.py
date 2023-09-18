import asyncio
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from Magic.helpers import *
from Magic import *
from config import *
from pytgcalls import GroupCallFactory

async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"**No group call Found** {err_msg}")
    return False

@ubot.on_message(filters.command("joinvc", prefix) & filters.me)
async def joinvc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    mmk = await message.edit("Joining....")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.vc.start(chat_id)
        await mmk.edit(f"**Successful joined the Voice Chat**\n└ **Chat ID**: {chat_id}")
        await asyncio.sleep(5)
        await client.vc.set_is_mute(True)
    except Exception as f:
        return await mmk.edit(f"ERROR: {f}")



@ubot.on_message(filters.command("leavevc", prefix) & filters.me)
async def leavevc(client, message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    mmk = await message.edit("`Leaving....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.vc.leave()
    except Exception as f:
        return await edit_or_reply(message, f"**ERROR:** `{f}`")
    msg = "**Successfully leave the Voice Chat**\n**"
    if chat_id:
        msg += f"\n└ **Chat ID:** `{chat_id}`"
    await mmk.edit(msg)      
