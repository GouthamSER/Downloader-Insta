from pyrogram import Client, filters
import requests
import re

# Function to extract Instagram Reel video URL
def extract_reel_url(url):
    try:
        response = requests.get(url)
        html = response.text
        pattern = r'"video_url":"(https:\/\/.*?\.mp4)"'
        match = re.search(pattern, html)
        if match:
            return match.group(1)
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Command to handle Instagram Reel link
@Client.on_message(filters.private & filters.regex(r'https?://(?:www\.)?instagram\.com/\S+/reel/\S+'))
async def handle_instagram_reel(bot, message):
    try:
        reel_url = message.text

        # Extract Reel video URL
        video_url = extract_reel_url(reel_url)

        if video_url:
            # Download video
            file_name = "reel_video.mp4"
            with open(file_name, "wb") as file:
                video_response = requests.get(video_url)
                file.write(video_response.content)

            # Send video to user
            await message.reply_video(video=file_name)

            # Delete downloaded file
            os.remove(file_name)

        else:
            await message.reply_text("Sorry, couldn't extract the Reel video.")

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
