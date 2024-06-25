import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import yt_dlp

# Define API credentials
api_id = '18979569'
api_hash = '45db354387b8122bdf6c1b0beef93743'
bot_token = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'

app = Client("youtube_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["start"]))
async def start(client, message):
    await message.reply_text("Hello! Send me a YouTube link to download the video or audio.")

@app.on_message(filters.text & ~filters.private)
async def download(client, message):
    url = message.text
    buttons = [
        [InlineKeyboardButton("Download Video", callback_data=f"video|{url}"),
         InlineKeyboardButton("Download Audio", callback_data=f"audio|{url}")]
    ]
    await message.reply_text("Choose format:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    choice, url = data.split("|")

    if choice == "video":
        await callback_query.message.reply_text("Downloading video...")
        video_path = await download_video(url)
        await client.send_video(callback_query.message.chat.id, video_path)
        os.remove(video_path)
    elif choice == "audio":
        await callback_query.message.reply_text("Downloading audio...")
        audio_path = await download_audio(url)
        await client.send_audio(callback_query.message.chat.id, audio_path)
        os.remove(audio_path)

    await callback_query.answer()

async def download_video(url):
    loop = asyncio.get_event_loop()
    video_path = await loop.run_in_executor(None, lambda: yt_dlp.download(url, format="mp4"))
    return video_path

async def download_audio(url):
    loop = asyncio.get_event_loop()
    audio_path = await loop.run_in_executor(None, lambda: yt_dlp.download(url, format="bestaudio"))
    return audio_path

def download_video(url, format="mp4"):
    ydl_opts = {
        'format': format,
        'outtmpl': '%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def download_audio(url, format="bestaudio"):
    ydl_opts = {
        'format': format,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)



if __name__ == "__main__":
    app.run()
