import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import instaloader
from pytube import YouTube

API_ID = '18979569'
API_HASH = '45db354387b8122bdf6c1b0beef93743'
BOT_TOKEN = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'

# Initialize the bot with your Telegram API credentials and bot token
app = Client("instagram_youtube_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to download Instagram post or reel video
def download_instagram_video(url):
    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        filename = f"{post.owner_username}_{post.shortcode}.mp4"
        L.download_post(post, target="downloads")
        return filename
    except instaloader.exceptions.QueryReturnedNotFoundException:
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to download YouTube video
async def download_youtube_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        return stream.download(output_path="downloads")
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to convert YouTube video to MP3
async def convert_to_mp3(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        output = stream.download(output_path="downloads")
        base, ext = os.path.splitext(output)
        new_file = base + '.mp3'
        os.rename(output, new_file)
        return new_file
    except Exception as e:
        print(f"Error: {e}")
        return None

# Handler for /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    message.reply_text("Hello! Send me an Instagram post or reel video URL, or a YouTube video link, and I'll download it for you.")

# Handler for messages containing Instagram or YouTube URLs
@app.on_message(filters.text & filters.private)
async def handle_urls(client, message):
    url = message.text
    if "instagram.com/p/" in url or "instagram.com/reel/" in url:
        buttons_instagram = [
            [InlineKeyboardButton("Download Video", callback_data=f"instagram|video|{url}")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons_instagram)
        message.reply_text("Choose an option for Instagram video:", reply_markup=reply_markup)
    elif "youtube.com/watch?" in url or "youtu.be" in url:
        buttons_youtube = [
            [InlineKeyboardButton("Download Video", callback_data=f"youtube|video|{url}")],
            [InlineKeyboardButton("Convert to MP3", callback_data=f"youtube|mp3|{url}")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons_youtube)
        message.reply_text("Choose an option for YouTube video:", reply_markup=reply_markup)
    else:
        message.reply_text("Please send a valid Instagram post or reel video URL, or a YouTube video link.")

# Handler for callback queries
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    platform, action, url = data.split('|')[0], data.split('|')[1], '|'.join(data.split('|')[2:])  # Reconstruct the URL part

    chat_id = callback_query.message.chat.id

    if platform == "instagram":
        if action == "video":
            callback_query.message.reply_text("Downloading the Instagram video, please wait...")
            file = download_instagram_video(url)
            if file:
                app.send_video(chat_id, f"downloads/{file}", reply_to_message_id=callback_query.message.message_id)
                os.remove(f"downloads/{file}")  # Clean up downloaded file
            else:
                callback_query.message.reply_text("Failed to download the Instagram video. Please check the link and try again.")
    elif platform == "youtube":
        if action == "video":
            callback_query.message.reply_text("Downloading the YouTube video, please wait...")
            file = download_youtube_video(url)
            if file:
                app.send_video(chat_id, f"downloads/{file}", reply_to_message_id=callback_query.message.message_id)
                os.remove(f"downloads/{file}")  # Clean up downloaded file
            else:
                callback_query.message.reply_text("Failed to download the YouTube video. Please check the link and try again.")
        elif action == "mp3":
            callback_query.message.reply_text("Converting the YouTube video to MP3, please wait...")
            file = convert_to_mp3(url)
            if file:
                app.send_audio(chat_id, f"downloads/{file}", reply_to_message_id=callback_query.message.message_id)
                os.remove(f"downloads/{file}")  # Clean up downloaded file
            else:
                callback_query.message.reply_text("Failed to convert the YouTube video to MP3. Please check the link and try again.")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run()
