from aiohttp import web as webserver
import tgcrypto
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
import pytz
from Script import script
from os import environ
from info import API_ID, API_HASH, BOT_TOKEN
from datetime import date, datetime 
from plugins.webcode import bot_run


bot = Client(
    name = "Instagram Downloader",
    api_id = "18979569",
    api_hash = "45db354387b8122bdf6c1b0beef93743",
    bot_token = "7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w"
)


print("BOT STARTED")

@bot.on_message(filters.command("start"))
async def start(client, message):
    
    button= [[
    InlineKeyboardButton("HELP✨", callback_data="help"),
    InlineKeyboardButton('About', callback_data="about")
]]        
    m=datetime.datetime.now()
    time=m.hour
    if time < 12:
        get="GoodMorning"
    elif time <16:
        get="Good Evening"
    else:
        get="Good Night"
    
    await message.reply_text(
        text=script.START_TXT.format(get,  message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(button)
    )

@bot.on_callback_query()
async def start(client, msg):
    
    if msg.data == "start":
        await msg.message.edit(
            text=script.START_TXT.format(get,  message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Help✨", callback_data="help"),
                InlineKeyboardButton("About", callback_data="about")
            ]]
            )
        )

    elif msg.data == "help":
        await msg.message.edit(
            text=script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Back", callback_data="start")
            ]]
            )
        )
    elif msg.data == "about":
        await msg.message.edit(
            text=script.ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton('Back', callback_data="start")
            ]]
            )
        )


@bot.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text(
        text=script.HELP_TXT
    )
    
@bot.on_message(filters.command("about"))
async def about(client, message):
    await message.reply_text(
        text=script.ABOUT_TXT
    )


@bot.on_message(filters.command("insta"))
async def start_command(client, message):
    await message.reply_text("Welcome! Send me an Instagram video link and I'll download and send it back to you.")

# Handler for text messages
@bot.on_message(filters.command)
async def private_message(client, message):
    # Check if the message contains an Instagram video URL
    if "instagram.com/p/" in message.text:
        try:
            # Extract the Instagram video URL
            video_url = message.text.strip()
            
            # Download the video from the Instagram post
            response = requests.get(video_url, stream=True)
            
            # Save the video to a file
            filename = "instagram_video.mp4"
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            
            # Send the video to the user
            await client.send_video(message.chat.id, video=filename)

        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")

bot.run()
