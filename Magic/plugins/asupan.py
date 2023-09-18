#TeamPesulap
#kyaa><


from asyncio import gather
from random import choice

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import *
from Magic import *

__MODULE__ = "Asupan"
__HELP__ = """
 Bantuan Untuk Asupan

• Perintah :  <code>{0}asupan</code>
• Penjelasan :  Untuk mengirim video asupan.
• Perintah : <code>{0}bokep</code>
• Penjelasan : Untuk mengirim video bokep random.
"""


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id


@ubot.on_message(filters.command("bkp", prefix) & filters.me)
async def bkp_cmd(client: Client, message: Message):
    uptt = await message.reply("`Tunggu Sebentar...`")
    await client.join_chat("punyapesulap")
    await gather(
    uptt.delete(),
      client.send_video(
      message.chat.id,
      choice(
              [
                bkp.video.file_id
                async for bkp in client.search_messages("punyapesulap", filter=enums.MessagesFilter.VIDEO)
              ]
            ),
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@ubot.on_message(filters.command("ayang", prefix) & filters.me)
async def ayang(client, message):
    uptt = await message.reply("🔎 `Search Ayang...`")
    anda = message.from_user.first_name
    dua = message.from_user.id
    await message.reply_photo(
        choice(
            [
                hha.photo.file_id
                async for hha in client.search_messages("CeweLogoPack", filter=enums.MessagesFilter.PHOTO)
            ]
        ),
        False,
        caption=f"Selingkuhannya [{anda}](tg://user?id={dua}) 🥰🤏",
    )

    await uptt.delete()


@ubot.on_message(filters.command("couple", prefix) & filters.me)
async def couple(client, message):
    uptt = await message.reply("🔎 `Search PP Couple...`")
    message.from_user.first_name
    message.from_user.id
    await message.reply_photo(
        choice(
            [
              awk.photo.file_id
              async for awk in client.search_messages("ppcpcilik", filter=enums.MessagesFilter.PHOTO)
            ]
        ),
        False,
        caption=f"PP Virtualmu nih dek!. 🤏",
    )

    await uptt.delete()
