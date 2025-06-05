import os
import asyncio
import time
from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from config import API_ID, API_HASH, BOT_TOKEN, DUMP_CHANNEL, ADMIN_USERS
from database import add_user, get_all_users, count_users
from fileFormat import (
    get_format_buttons,
    get_delivery_type_buttons,
    get_video_quality_buttons,
    get_audio_quality_buttons,
)
from handlers.singleVideo import download_video
from handlers.singleAudio import download_audio
from handlers.playlistVideo import download_playlist_video
from handlers.playlistAudio import download_playlist_audio

user_data = {}

app = Client("yt_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    user_id = message.from_user.id
    add_user(user_id, message.from_user.username, message.from_user.first_name)
    await client.send_message(
        DUMP_CHANNEL,
        f"#NEW_USER\nID: `{user_id}`\nName: {message.from_user.first_name}\nUsername: @{message.from_user.username}"
    )
    await message.reply("👋 Welcome to YouTube Downloader Bot!\n\nSend any YouTube link to download video or audio.")

@app.on_message(filters.command("help"))
async def help_handler(client, message: Message):
    await message.reply(
        "**How to Use:**\n"
        "1. Send a YouTube link.\n"
        "2. Choose format: MP4 or MP3.\n"
        "3. Choose quality.\n"
        "4. Choose how to receive: File or Document.\n"
        "5. Bot will upload your file here.\n\n"
        "Supports both Single Videos and Playlists."
    )

@app.on_message(filters.command("settings"))
async def settings_handler(client, message: Message):
    await message.reply("Choose format:", reply_markup=get_format_buttons())

@app.on_message(filters.command("users") & filters.user(ADMIN_USERS))
async def users_handler(client, message: Message):
    total = count_users()
    await message.reply(f"👤 Total Users: `{total}`")

@app.on_message(filters.command("status") & filters.user(ADMIN_USERS))
async def status_handler(client, message: Message):
    await message.reply("✅ Bot is up and running!")

@app.on_message(filters.command("broadcast") & filters.user(ADMIN_USERS))
async def broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to a message to broadcast.")
    users = get_all_users()
    sent = 0
    for user in users:
        try:
            await client.send_message(user["_id"], message.reply_to_message.text)
            sent += 1
            await asyncio.sleep(0.1)
        except:
            continue
    await message.reply(f"✅ Broadcast sent to `{sent}` users.")

@app.on_message(filters.text & filters.private)
async def handle_youtube_url(client, message: Message):
    url = message.text.strip()
    if not ("youtube.com" in url or "youtu.be" in url):
        return await message.reply("⚠️ Invalid YouTube URL.")
    user_data[message.from_user.id] = {"url": url}
    await message.reply("📦 Choose format:", reply_markup=get_format_buttons())

@app.on_callback_query(filters.regex("format_"))
async def format_callback(client, callback_query: CallbackQuery):
    format_type = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        return await callback_query.message.edit("❌ Session expired. Please send the URL again.")
    user_data[user_id]["format"] = format_type

    if format_type == "mp4":
        await callback_query.message.edit("📽 Choose video quality:", reply_markup=get_video_quality_buttons())
    else:
        await callback_query.message.edit("🎵 Choose audio quality:", reply_markup=get_audio_quality_buttons())

@app.on_callback_query(filters.regex("^(video|audio)_"))
async def quality_callback(client, callback_query: CallbackQuery):
    quality_value = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        return await callback_query.message.edit("❌ Session expired. Please send the URL again.")

    user_data[user_id]["quality"] = quality_value
    await callback_query.message.edit("📤 Choose delivery type:", reply_markup=get_delivery_type_buttons())

@app.on_callback_query(filters.regex("as_"))
async def delivery_callback(client, callback_query: CallbackQuery):
    delivery = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    data = user_data.get(user_id)

    if not data or "url" not in data or "format" not in data or "quality" not in data:
        return await callback_query.message.edit("❌ Session expired. Please send the URL again.")

    url = data["url"]
    file_format = data["format"]
    quality = data["quality"]
    is_doc = delivery == "document"

    await callback_query.message.edit("⏳ Downloading... Please wait.")

    try:
        if "playlist" in url.lower():
            if file_format == "mp4":
                files = download_playlist_video(url, quality)
            else:
                files = download_playlist_audio(url, quality)

            await upload_playlist_files(client, callback_query.message.chat.id, files, file_format, is_doc)
            await callback_query.message.reply("✅ Playlist files uploaded!")
        else:
            if file_format == "mp4":
                file_obj = download_video(url, quality)
            else:
                file_obj = download_audio(url, quality)

            start_time = time.time()
            uploading_msg = await callback_query.message.reply("📤 Uploading...")

            caption = f"🎬 `{getattr(file_obj, 'name', 'video')}`"
            if file_format == "mp4" and not is_doc:
                await client.send_video(
                    chat_id=callback_query.message.chat.id,
                    video=file_obj,
                    caption=caption,
                    progress=progress_bar,
                    progress_args=(uploading_msg, start_time)
                )
            else:
                await client.send_document(
                    chat_id=callback_query.message.chat.id,
                    document=file_obj,
                    caption=caption,
                    progress=progress_bar,
                    progress_args=(uploading_msg, start_time)
                )
            await client.send_document(DUMP_CHANNEL, document=file_obj, caption=f"User: `{user_id}` | {file_format.upper()}")

            await uploading_msg.delete()
    except Exception as e:
        return await callback_query.message.edit(f"❌ Failed: `{e}`")

    user_data.pop(user_id, None)

async def upload_playlist_files(client, chat_id, file_paths, file_format, is_doc):
    for file_path in file_paths:
        try:
            if file_format == "mp4" and not is_doc:
                await client.send_video(chat_id=chat_id, video=file_path)
            else:
                await client.send_document(chat_id=chat_id, document=file_path)
        except Exception as e:
            print(f"Failed to upload {file_path}: {e}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

async def progress_bar(current, total, message: Message, start):
    now = time.time()
    diff = now - start
    if diff == 0 or (diff > 0 and (int(diff) % 2 == 0 or current == total)):
        percent = current * 100 / total if total else 0
        speed = current / diff if diff else 0
        eta = (total - current) / speed if speed else 0
        bar_length = 20
        filled_length = int(bar_length * current // total) if total else 0
        bar = "▰" * filled_length + "▱" * (bar_length - filled_length)
        await message.edit(
            f"📤 Uploading...\n"
            f"[{bar}] {percent:.2f}%\n"
            f"{current / 1024 / 1024:.2f}MB of {total / 1024 / 1024:.2f}MB\n"
            f"Speed: {speed / 1024:.2f} KB/s\n"
            f"ETA: {int(eta)}s"
        )

if __name__ == "__main__":
    app.run()