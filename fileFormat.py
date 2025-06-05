from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_format_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎞 MP4 (Video)", callback_data="format_mp4"),
            InlineKeyboardButton("🎧 MP3 (Audio)", callback_data="format_mp3")
        ]
    ])

def get_delivery_type_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📤 Send as File", callback_data="as_file"),
            InlineKeyboardButton("🗂 Send as Document", callback_data="as_document")
        ]
    ])