from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from config import API_ID, API_HASH, BOT_TOKEN, DUMP_CHANNEL, ADMIN_USERS
from database import add_user, get_all_users, count_users
from fileFormat import get_format_buttons, get_delivery_type_buttons

from handlers.singleVideo import download_video
from handlers.singleAudio import download_audio

import os
import asyncio

user_data = {}

app = Client("yt_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    user_id = message.from_user.id
    add_user(user_id, message.from_user.username, message.from_user.first_name)
    await client.send_message(
        DUMP_CHANNEL,
        f"#NEW_USER\nID: `{user_id}`\nName: {message.from_user.first_name}\nUsername: @{message.from_user.username}"
    )
    await message.reply("👋 Welcome to YouTube Downloader Bot!\n\nSend any YouTube link to download video or audio.")

# Help Command
@app.on_message(filters.command("help"))
async def help_handler(client, message: Message):
    await message.reply(
        "**How to Use:**\n"
        "1. Send a YouTube link.\n"
        "2. Choose format: MP4 or MP3.\n"
        "3. Choose how to receive: File or Document.\n"
        "4. Bot will upload your file here.\n\n"
        "Supports both Single Videos and Playlists."
    )

# Settings
@app.on_message(filters.command("settings"))
async def settings_handler(client, message: Message):
    await message.reply("Choose format:", reply_markup=get_format_buttons())

# Admin: Users
@app.on_message(filters.command("users") & filters.user(ADMIN_USERS))
async def users_handler(client, message: Message):
    total = count_users()
    await message.reply(f"👤 Total Users: `{total}`")

# Admin: Status
@app.on_message(filters.command("status") & filters.user(ADMIN_USERS))
async def status_handler(client, message: Message):
    await message.reply("✅ Bot is up and running!")

# Admin: Broadcast
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

# Handle URLs
@app.on_message(filters.text & filters.private)
async def handle_youtube_url(client, message: Message):
    url = message.text.strip()
    if not ("youtube.com" in url or "youtu.be" in url):
        return await message.reply("⚠️ Invalid YouTube URL.")
    user_data[message.from_user.id] = {"url": url}
    await message.reply("📦 Choose format:", reply_markup=get_format_buttons())

# Callback for format (mp4/mp3)
@app.on_callback_query(filters.regex("format_"))
async def format_callback(client, callback_query: CallbackQuery):
    format_type = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    if user_id not in user_data:
        return await callback_query.message.edit("❌ Session expired. Please send the URL again.")
    user_data[user_id]["format"] = format_type
    await callback_query.message.edit("📤 Choose delivery type:", reply_markup=get_delivery_type_buttons())

# Callback for delivery type
@app.on_callback_query(filters.regex("as_"))
async def delivery_callback(client, callback_query: CallbackQuery):
    delivery = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    data = user_data.get(user_id)

    if not data or "url" not in data or "format" not in data:
        return await callback_query.message.edit("❌ Session expired. Please send the URL again.")

    url = data["url"]
    file_format = data["format"]
    is_doc = delivery == "document"

    await callback_query.message.edit("⏳ Downloading... Please wait.")

    try:
        if file_format == "mp4":
            filepath = download_video(url)
        elif file_format == "mp3":
            filepath = download_audio(url)
        else:
            return await callback_query.message.edit("⚠️ Invalid format selected.")
    except Exception as e:
        return await callback_query.message.edit(f"❌ Download failed:\n`{e}`")

    try:
        caption = f"🎬 `{os.path.basename(filepath)}`"
        await callback_query.message.reply_document(
            document=filepath if is_doc else filepath,
            caption=caption
        ) if is_doc else await callback_query.message.reply_video(video=filepath, caption=caption)

        # Log download to dump channel
        await client.send_document(DUMP_CHANNEL, document=filepath, caption=f"User: `{user_id}` | {file_format.upper()}")
    except Exception as e:
        await callback_query.message.edit(f"⚠️ Upload failed:\n`{e}`")
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
        user_data.pop(user_id, None)

# Run the bot
app.run()