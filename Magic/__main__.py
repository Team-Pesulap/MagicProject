import asyncio
import importlib

import logging
from pyrogram import idle
from Magic import *
from Magic.helpers import *
from Magic.helpers._database import *
#from Magic.assistant import ALL_SETTINGS
from Magic.plugins import ALL_MODULES

from uvloop import install

HELP_COMMANDS = {}


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def done():
    try:
        await ubot.join_chat("pesulaptelegram")
        await ubot.send_message(-1001861414061, "Halo... Aku Berhasil Mengaktifkan Userbot")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    await bot.start()
    #for x in ALL_SETTINGS:
        #imported_module = importlib.import_module("Magic.assistant." + x)
        #importlib.reload(imported_module)
    await ubot.start()
    for xx in ALL_MODULES:
        imported_module = importlib.import_module("Magic.plugins." + xx)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if not imported_module.__MODULE__.lower() in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
            else:
                raise Exception("Double Plugins Detected.")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
    ubot_mod = ""
    bot_mod = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            ubot_mod += "|{:<15}|\n".format(i)
            j = 0
        else:
            ubot_mod += "|{:<15}".format(i)
        j += 1
    j = 1
    print("+===============================================================+")
    print("|                      Userbot Modules                          |")
    print("+===============+===============+===============+===============+")
    print(ubot_mod)
    print("+===============+===============+===============+===============+\n")
    print("+===============================================================+")
    print("|                    Assistant Modules                          |")
    print("+===============+===============+===============+===============+")
    #print(bot_ubot)
    print("+===============+===============+===============+===============+")
    print("Berhasil Menginstall Plugins")
    try:
        print(f"Koneksi Ke Database {MDB.name}...")
        if MDB.ping():
            print(f"Koneksi Berhasil Ke {MDB.name}..")
            xxx = (await ubot.get_me()).id
            MDB.set_key("OWNER_ID", ubot.me.id)
        await done()
        await idle()
        await aiosession.close()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
"""
if __name__ == "__main__":
    install()
    heroku()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
"""

if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())
