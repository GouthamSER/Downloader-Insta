from Script import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re


@Client.on_message(filters.command("start"))
async def start(bot, message):
    
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

@Client.on_callback_query()
async def start(bot, msg):
    
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


@Client.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply_text(
        text=script.HELP_TXT
    )
    
@Client.on_message(filters.command("about"))
async def about(bot, message):
    await message.reply_text(
        text=script.ABOUT_TXT
    )


@Client.on_message(filters.command("insta"))
async def start_command(bot, message):
    await message.reply_text("Welcome! Send me an Instagram video link and I'll download and send it back to you.")

# Handler for text messages
@Client.on_message(filters.command)
async def private_message(bot, message):
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
            await bot.send_video(message.chat.id, video=filename)

        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")
