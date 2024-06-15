import os
import instaloader
from pyrogram import Client, filters

# Telegram API credentials
API_ID = '18979569'
API_HASH = '45db354387b8122bdf6c1b0beef93743'
BOT_TOKEN = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'

# Initialize Instaloader
L = instaloader.Instaloader()

# Initialize the bot with your Telegram API credentials and bot token
app = Client("insta_reel_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to download Instagram Reels video
def download_instagram_reel(url):
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        if post.typename == "GraphVideo":  # Check if the post is a video (Reel)
            L.download_post(post, target="downloads")
            for file in os.listdir("downloads"):
                if file.endswith(".mp4"):
                    return os.path.join("downloads", file)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Handler for /start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! Send me an Instagram Reels link, and I'll download it for you.")

# Handler for messages containing Instagram Reels links
@app.on_message(filters.text & filters.private)
def download_reel(client, message):
    url = message.text
    if "instagram.com/reel" in url:
        message.reply_text("Downloading the Reels video, please wait...")
        video_path = download_instagram_reel(url)
        if video_path:
            message.reply_video(video_path)
            # Clean up downloaded file
            os.remove(video_path)
        else:
            message.reply_text("Failed to download the Reels video. Please check the link and try again.")
    else:
        message.reply_text("Please send a valid Instagram Reels link.")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run()
