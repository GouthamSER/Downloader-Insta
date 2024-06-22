import os

import asyncio

from pyrogram import Client, filters

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytube import YouTube

import instaloader

from pydub import AudioSegment

from aiomultiprocess import Pool



# Initialize Telegram Bot

api_id = '18979569'

api_hash = '45db354387b8122bdf6c1b0beef93743'

bot_token = '7195222206:AAGsp4RstBtnChHAx_aQNNV-PJ6_cQEE54w'



app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)



# Asynchronously Download and Convert YouTube Video or MP3

async def download_youtube(url, download_type):

    yt = YouTube(url)

    if download_type == 'video':

        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        file_path = stream.download()

    elif download_type == 'mp3':

        stream = yt.streams.filter(only_audio=True).first()

        file_path = stream.download()

        audio = AudioSegment.from_file(file_path)

        mp3_path = file_path.replace('.mp4', '.mp3')

        audio.export(mp3_path, format='mp3')

        os.remove(file_path)

        file_path = mp3_path

    return file_path



# Asynchronously Download Instagram Content

async def download_instagram(url):

    loader = instaloader.Instaloader()

    post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])

    if post.typename == "GraphVideo":

        loader.download_post(post, target="downloads")

    else:

        loader.download_post(post, target="downloads")

    return "downloads"



# Start Command

@app.on_message(filters.command("start"))

async def start(client, message):

    await message.reply("Welcome! Send me a YouTube or Instagram link.")



# YouTube Link Handler

@app.on_message(filters.regex(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'))

async def youtube_handler(client, message):

    url = message.text

    buttons = [

        [InlineKeyboardButton("Download Video", callback_data=f"yt_video|{url}"),

         InlineKeyboardButton("Download MP3", callback_data=f"yt_mp3|{url}")]

    ]

    await message.reply("Choose download type:", reply_markup=InlineKeyboardMarkup(buttons))



# Instagram Link Handler

@app.on_message(filters.regex(r'^(https?\:\/\/)?(www\.instagram\.com)\/.+$'))

async def instagram_handler(client, message):

    url = message.text

    async with Pool() as pool:

        file_path = await pool.apply(download_instagram, (url,))

    await message.reply_document(document=file_path)



# Callback Query Handler

@app.on_callback_query()

async def callback_query_handler(client, callback_query):

    data = callback_query.data

    download_type, url = data.split('|')

    chat_id = callback_query.message.chat.id



    async with Pool() as pool:

        file_path = await pool.apply(download_youtube, (url, download_type))



    await client.send_document(chat_id, file_path)

    os.remove(file_path)



if __name__ == "__main__":

    app.run()

