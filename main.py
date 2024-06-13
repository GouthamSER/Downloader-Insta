import os
import tgcrypto
import requests
from pyrogram import Client, filters

# Initialize your Pyrogram client
api_id = "18979569"
api_hash = "45db354387b8122bdf6c1b0beef9374"
bot_token = "7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w"

app = Client("instagram_bot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)


# Handler for the /start command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Welcome! Send me an Instagram video link and I'll download and send it back to you."
    )


# Handler for text messages
@app.on_message(filters.command)
async def private_message(client, message):
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
            await client.send_video(message.chat.id, video=filename)

        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")


# Start the bot
app.run()
