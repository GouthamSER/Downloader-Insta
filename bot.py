import os
import instaloader
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube

# Telegram API credentials
API_ID = '18979569'
API_HASH = '45db354387b8122bdf6c1b0beef93743'
BOT_TOKEN = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'

# Initialize Instaloader
L = instaloader.Instaloader()

# Initialize the bot with your Telegram API credentials and bot token
app = Client("downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to download Instagram content
def download_instagram_content(url):
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        L.download_post(post, target="downloads")
        files = []
        for file in os.listdir("downloads"):
            if file.endswith(".mp4") or file.endswith(".jpg"):
                files.append(os.path.join("downloads", file))
        return files
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to download YouTube video
def download_youtube_video(url, download_audio=False):
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
            stream = yt.streams.get_highest_resolution()
            return stream.download(output_path="downloads")
    except Exception as e:
        print(f"Error: {e}")
        return None

# Handler for /start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me an Instagram Reels or post link, or a YouTube video link, and I'll download it for you. For YouTube, you'll get an option to choose 'video' or 'mp3'.")

# Handler for messages containing Instagram links
@app.on_message(filters.text & filters.private)
def handle_links(client, message):
    url = message.text
    if "instagram.com/reel" in url or "instagram.com/p" in url:
        message.reply_text("Downloading the Instagram content, please wait...")
        files = download_instagram_content(url)
        if files:
            for file in files:
                if file.endswith(".mp4"):
                    message.reply_video(file)
                elif file.endswith(".jpg"):
                    message.reply_photo(file)
                os.remove(file)  # Clean up downloaded file
        else:
            message.reply_text("Failed to download the Instagram content. Please check the link and try again.")
    elif "youtube.com" in url or "youtu.be" in url:
        buttons = [
            [
                InlineKeyboardButton("Download Video", callback_data=f"video|{url}"),
                InlineKeyboardButton("Download MP3", callback_data=f"mp3|{url}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        message.reply_text("Choose the format to download:", reply_markup=reply_markup)
    else:
        message.reply_text("Please send a valid Instagram Reels, post link, or YouTube link.")

# Handler for callback queries
@app.on_callback_query()
def callback_query_handler(client, callback_query):
    data = callback_query.data
    action, url = data.split('|')

    if action == "video":
        callback_query.message.reply_text("Downloading the YouTube video, please wait...")
        file = download_youtube_video(url, download_audio=False)
        if file:
            callback_query.message.reply_video(file)
            os.remove(file)  # Clean up downloaded file
        else:
            callback_query.message.reply_text("Failed to download the YouTube video. Please check the link and try again.")
    elif action == "mp3":
        callback_query.message.reply_text("Downloading the YouTube audio, please wait...")
        file = download_youtube_video(url, download_audio=True)
        if file:
            callback_query.message.reply_audio(file)
            os.remove(file)  # Clean up downloaded file
        else:
            callback_query.message.reply_text("Failed to download the YouTube audio. Please check the link and try again.")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run()
