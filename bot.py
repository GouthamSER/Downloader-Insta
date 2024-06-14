from aiohttp import web as webserver
from plugins.webcode import bot_run
import tgcrypto
from pyrogram import Client, __version__, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw.all import layer
import pytz
from Script import script
from os import environ
from info import API_ID, API_HASH, BOT_TOKEN
from datetime import date, datetime 

PORT_CODE = environ.get("PORT", "8080")

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="InstaBOT",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        print("Recoded By Goutham SER </>")

        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        print(today, time)
        #await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
        
        client = webserver.AppRunner(await bot_run())
        await client.setup()
        bind_address = "0.0.0.0"
        await webserver.TCPSite(client, bind_address,
        PORT_CODE).start()
        
        

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")


app = Bot()
app.run()
