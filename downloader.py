import os
import requests
from pyrogram import Client, filters
from pytube import YouTube
import youtube_dl


# Function to download Instagram video
def download_instagram_video(instagram_url):
    try:
        # Use an Instagram video downloader API (replace with a real API)
        api_url = 'https://api.instagramdownloader.com?url=' + instagram_url
        response = requests.get(api_url)
        if response.status_code == 200:
            video_url = response.json().get('video_url')
            return video_url
    except Exception as e:
        print(f"Error: {e}")
    return None

# Function to download YouTube video
def download_youtube_video(url, quality='highest'):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
    if quality == 'lowest':
        stream = yt.streams.filter(file_extension='mp4').order_by('resolution').asc().first()
    video_path = stream.download()
    return video_path

# Function to download YouTube video as MP3
def download_youtube_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(result)
        mp3_path = filename.rsplit('.', 1)[0] + '.mp3'
    return mp3_path

@Client.on_message(filters.command(["start"]))
async def start(bot, message):
    await message.reply("Send me an Instagram video link or a YouTube video link and I will download it for you! You can also specify 'lowest' or 'highest' quality for YouTube videos, or ask to convert to MP3.")

@Client.on_message(filters.text & ~filters.command)
async def handle_message(bot, message):
    text = message.text
    if 'instagram.com' in text:
        await message.reply("Downloading Instagram video...")
        video_url = download_instagram_video(text)
        if video_url:
            await bot.send_video(chat_id=message.chat.id, video=video_url)
        else:
            await message.reply("Failed to download the Instagram video.")
    elif 'youtube.com' in text or 'youtu.be' in text:
        parts = text.split()
        url = parts[0]
        option = parts[1] if len(parts) > 1 else 'highest'
        if option == 'mp3':
            await message.reply("Downloading YouTube video as MP3...")
            mp3_path = download_youtube_mp3(url)
            await bot.send_audio(chat_id=message.chat.id, audio=mp3_path)
            os.remove(mp3_path)
        else:
            await message.reply(f"Downloading YouTube video in {option} quality...")
            video_path = download_youtube_video(url, option)
            await bot.send_video(chat_id=message.chat.id, video=video_path)
            os.remove(video_path)
    else:
        await message.reply("Please send a valid Instagram or YouTube video link.")

app.run()