import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import youtube_dl
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace these with your own values
api_id = '18979569'
api_hash = '45db354387b8122bdf6c1b0beef93743'
bot_token = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'

# Initialize the bot
app = Client("my_youtube_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to download video or audio
async def download_youtube_content(url, content_type):
    download_path = f"downloads/{int(asyncio.time())}"
    os.makedirs(download_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best' if content_type == 'audio' else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if content_type == 'audio' else [],
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'quiet': True,
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return download_path
    except Exception as e:
        logging.error(f"Error downloading content: {e}")
        return None

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Send me a YouTube link and choose whether to download it as video or audio!")

@app.on_message(filters.regex(r'^https?://(www\.)?(youtube\.com|youtu\.be)/.+$'))
async def youtube_handler(client, message):
    url = message.text
    await message.reply("What would you like to download?\n\n1. Video\n2. Audio", 
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Video", callback_data=f"video|{url}")],
                            [InlineKeyboardButton("Audio", callback_data=f"audio|{url}")]
                        ]))

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data.split("|")
    content_type = data[0]
    url = data[1]

    await callback_query.message.edit_text(f"Downloading the {content_type}...")

    download_path = await download_youtube_content(url, content_type)
    if download_path:
        for root, _, files in os.walk(download_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    await client.send_document(callback_query.message.chat.id, file_path)
        
        await callback_query.message.edit_text("Download complete! The files will be deleted in 5 minutes.")
        
        # Schedule deletion of the temporary directory
        await asyncio.sleep(300)
        shutil.rmtree(download_path, ignore_errors=True)
    else:
        await callback_query.message.edit_text("Failed to download the content. Please check the URL and try again.")

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run()
