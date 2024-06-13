from aiohttp import web as webserver
import tgcrypto
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
import pytz
from os import environ
from info import API_ID, API_HASH, BOT_TOKEN
from datetime import date, datetime 



PORT_CODE = environ.get("PORT", "8080")

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="InstaBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        print(f"Instagram Downloader Bot with for Pyrogram v{__version__} (Layer {layer}) started on @Kuttudownloader_bot.")
        print("Recoded By Goutham SER </>")
        print("THIS IS InsTA VIDEO DOWNLOADER BOT")


        
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
