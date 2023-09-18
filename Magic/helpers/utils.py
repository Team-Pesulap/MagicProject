import os
from pyrogram import Client, emoji, filters
from pyrogram.types import Message

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

def get_args(message: Message):
    try:
        message = message.text
    except AttributeError:
        pass
    if not message:
        return False
    message = message.split(maxsplit=1)
    if len(message) <= 1:
        return []
    message = message[1]
    try:
        split = shlex.split(message)
    except ValueError:
        return message
    return list(filter(lambda x: len(x) > 0, split))
    
async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    anu = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await anu(*args, **kwargs)

async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    kontol = text.strip()

    if is_int(kontol):
        return int(kontol)

    meledak = message.entities
    kocok = message._client
    if len(entities) < 2:
        return (await kocok.get_users(kontol)).id
    mmk = meledak[1]
    if mmk.type == "mention":
        return (await kocok.get_users(kontol)).id
    if mmk.type == "text_mention":
        return mmk.user.id
    return None

async def extract_user(message):
    return (await extract_user_and_reason(message))[0]

import os
from pyrogram import Client, emoji, filters
from pyrogram.types import Message

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

def get_args(message: Message):
    try:
        message = message.text
    except AttributeError:
        pass
    if not message:
        return False
    message = message.split(maxsplit=1)
    if len(message) <= 1:
        return []
    message = message[1]
    try:
        split = shlex.split(message)
    except ValueError:
        return message
    return list(filter(lambda x: len(x) > 0, split))
    
async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    anu = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await anu(*args, **kwargs)

async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    kontol = text.strip()

    if is_int(kontol):
        return int(kontol)

    meledak = message.entities
    kocok = message._client
    if len(entities) < 2:
        return (await kocok.get_users(kontol)).id
    mmk = meledak[1]
    if mmk.type == "mention":
        return (await kocok.get_users(kontol)).id
    if mmk.type == "text_mention":
        return mmk.user.id
    return None

async def extract_user(message):
    return (await extract_user_and_reason(message))[0]

async def extract_user_and_reason(message, sender_chat=False):
    anu = message.text.strip().split()
    anuan = message.text
    orang = None
    alasan = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                mmk = reply.sender_chat.id
            else:
                return None, None
        else:
            mmk = reply.from_user.id

        if len(anu) < 2:
            alasan = None
        else:
            alasan = anuan.split(None, 1)[1]
        return mmk, alasan

    if len(anu) == 2:
        orang = anuan.split(None, 1)[1]
        return await extract_userid(message, orang), None

    if len(anu) > 2:
        orang, alasan = anuan.split(None, 2)[1:]
        return await extract_userid(message, orang), alasan

    return orang, alasan
