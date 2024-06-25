import os
import logging
import asyncio
from pyrogram import Client, filters
import instaloader
from instaloader import Profile
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace these with your own values
api_id = '18979569'
api_hash = '45db354387b8122bdf6c1b0beef93743'
bot_token = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'

# Initialize the bot
app = Client("my_instagram_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize Instaloader
loader = instaloader.Instaloader()

async def download_instagram_content(url):
    download_path = f"downloads/{int(asyncio.time())}"
    os.makedirs(download_path, exist_ok=True)
    
    try:
        if "/p/" in url or "/reel/" in url:
            post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
            loader.download_post(post, target=download_path)
        elif "/stories/" in url:
            username = url.split("/")[-2]
            profile = Profile.from_username(loader.context, username)
            for story in loader.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    loader.download_storyitem(item, target=f"{download_path}/{username}_stories")
        else:
            raise ValueError("Unsupported URL")
        return download_path
    except Exception as e:
        logging.error(f"Error downloading content: {e}")
        return None

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Send me an Instagram reel, post, or story link, and I'll download it for you!")

@app.on_message(filters.regex(r'^(https?://)?(www\.)?(instagram\.com|instagr\.am)/(p|reel|stories)/[a-zA-Z0-9_-]+/?$'))
async def instagram_handler(client, message):
    url = message.text
    await message.reply("Downloading the Instagram content...")

    download_path = await download_instagram_content(url)
    if download_path:
        for root, _, files in os.walk(download_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    await client.send_document(message.chat.id, file_path)
        
        await message.reply("Download complete! The files will be deleted in 5 minutes.")
        
        # Schedule deletion of the temporary directory
        await asyncio.sleep(300)
        shutil.rmtree(download_path, ignore_errors=True)
    else:
        await message.reply("Failed to download the content. Please check the URL and try again.")

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run()
