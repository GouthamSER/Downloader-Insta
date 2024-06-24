import os
import logging
import asyncio
from pyrogram import Client, filters
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace these with your own values
api_id = '18979569'
api_hash = '45db354387b8122bdf6c1b0beef93743'
bot_token = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'
spotify_client_id = 'e3023850cb7b45f1b0c500187afb942d'
spotify_client_secret = 'face7ba8168a4d8cae483c87dc37f7af'

# Initialize the bot
app = Client("my_spotify_bot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)

# Initialize Spotify client
spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spotify_client_id, client_secret=spotify_client_secret))


# Function to download song as MP3
async def download_song(query):
    ydl_opts = {
        'format':
        'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl':
        'downloads/%(title)s.%(ext)s',
        'quiet':
        True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_name = ydl.prepare_filename(info_dict)
        return file_name.replace(".webm", ".mp3").replace(".m4a", ".mp3")


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "Hello! Send me a Spotify link and I'll download the song for you as an MP3!"
    )


@app.on_message(
    filters.regex(
        r'^(https?://)?(www\.)?(open\.spotify\.com)/track/[a-zA-Z0-9]+$'))
async def spotify_handler(client, message):
    url = message.text
    await message.reply("Processing the Spotify link...")

    # Extract track info
    track_id = url.split("/")[-1].split("?")[0]
    track = spotify.track(track_id)
    track_name = track['name']
    track_artists = ", ".join(artist['name'] for artist in track['artists'])
    search_query = f"{track_name} {track_artists}"

    await message.reply(f"Downloading {track_name} by {track_artists}...")

    # Download song
    mp3_file = await download_song(search_query)

    if mp3_file:
        await client.send_audio(message.chat.id, audio=mp3_file)
        await message.reply("Download complete!")
    else:
        await message.reply(
            "Failed to download the song. Please try again later.")


if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run()
