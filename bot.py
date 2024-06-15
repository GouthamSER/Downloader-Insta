import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube

# Telegram API credentials
API_ID = '18979569'
API_HASH = '45db354387b8122bdf6c1b0beef93743'
BOT_TOKEN = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'

# Initialize the bot with your Telegram API credentials and bot token
app = Client("downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to download YouTube video or audio
def download_youtube(url, itag=None, download_audio=False):
    try:
        yt = YouTube(url)
        if download_audio:
            stream = yt.streams.filter(only_audio=True).first()
            output = stream.download(output_path="downloads")
            base, ext = os.path.splitext(output)
            new_file = base + '.mp3'
            os.rename(output, new_file)
            return new_file
        else:
            if itag:
                stream = yt.streams.get_by_itag(itag)
            else:
                stream = yt.streams.get_highest_resolution()
            return stream.download(output_path="downloads")
    except Exception as e:
        print(f"Error: {e}")
        return None

# Handler for /start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me a YouTube video link, and I'll give you options to download it as video or MP3.")

# Handler for messages containing YouTube links
@app.on_message(filters.text & filters.private)
def handle_youtube_link(client, message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        buttons = [
            [InlineKeyboardButton("Download MP3", callback_data=f"mp3|{url}")],
            [InlineKeyboardButton("Download Video", callback_data=f"video|{url}")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        message.reply_text("Choose the format to download:", reply_markup=reply_markup)
    else:
        message.reply_text("Please send a valid YouTube link.")

# Handler for callback queries
@app.on_callback_query()
def callback_query_handler(client, callback_query):
    data = callback_query.data
    action = data.split('|')[0]
    url = '|'.join(data.split('|')[1:])  # Reconstruct the URL part

    if action == "video":
        yt = YouTube(url)
        buttons = []
        for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
            buttons.append([InlineKeyboardButton(f"{stream.resolution} - {stream.fps}fps", callback_data=f"res|{stream.itag}|{url}")])
        reply_markup = InlineKeyboardMarkup(buttons)
        callback_query.message.reply_text("Choose the resolution to download:", reply_markup=reply_markup)
    elif action == "mp3":
        yt = YouTube(url)
        buttons = [
            [InlineKeyboardButton("High Quality", callback_data=f"mp3_high|{url}")],
            [InlineKeyboardButton("Medium Quality", callback_data=f"mp3_medium|{url}")],
            [InlineKeyboardButton("Low Quality", callback_data=f"mp3_low|{url}")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        callback_query.message.reply_text("Choose the MP3 quality to download:", reply_markup=reply_markup)
    elif action.startswith("res"):
        _, itag, url = action.split('|')
        callback_query.message.reply_text("Downloading the YouTube video, please wait...")
        file = download_youtube(url, itag=itag)
        if file:
            callback_query.message.reply_video(file)
            os.remove(file)  # Clean up downloaded file
        else:
            callback_query.message.reply_text("Failed to download the YouTube video. Please check the link and try again.")
    elif action.startswith("mp3"):
        quality = action.split('_')[1]
        callback_query.message.reply_text(f"Downloading the YouTube audio in {quality} quality, please wait...")
        if quality == 'high':
            file = download_youtube(url, download_audio=True)
        elif quality == 'medium':
            file = download_youtube(url, download_audio=True)  # Here you can add logic to convert to medium quality if needed
        elif quality == 'low':
            file = download_youtube(url, download_audio=True)  # Here you can add logic to convert to low quality if needed
        if file:
            callback_query.message.reply_audio(file)
            os.remove(file)  # Clean up downloaded file
        else:
            callback_query.message.reply_text("Failed to download the YouTube audio. Please check the link and try again.")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run()
