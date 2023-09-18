
from pyrogram import *

import pytgcalls
import config

CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM

INPUT_FILENAME = 'input.raw'
OUTPUT_FILENAME = 'output.raw'
OUTGOING_AUDIO_BITRATE_KBIT = 128

class MPUser(Client):
    def __init__(self):
        super().__init__(
            name="ubot",
            api_hash=config.API_HASH,
            api_id=config.API_ID,
            session_string=config.SESSION,
            in_memory=True,
            device_model="MagicProject",
            plugins=dict(root="Magic/plugins"),
        )
        self.vc = pytgcalls.GroupCallFactory(
            self, CLIENT_TYPE, OUTGOING_AUDIO_BITRATE_KBIT
            ).get_file_group_call(INPUT_FILENAME, OUTPUT_FILENAME)

    async def start(self):
        await super().start()
        x = self.me
        print(f"Started User As @{x.username} | {x.id}")

    async def stop(self, *args):
        await super().stop()
        
        
class MPBot(Client):
    def __init__(self):
        super().__init__(
            name="ubot",
            api_hash=config.API_HASH,
            api_id=config.API_ID,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            plugins=dict(root="Magic/asisstant"),
        )

    async def start(self):
        await super().start()
        x = self.me
        print(f"Started Bot As @{x.username} | {x.id}")

    async def stop(self, *args):
        await super().stop()
