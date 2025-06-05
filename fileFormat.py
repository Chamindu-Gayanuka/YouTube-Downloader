from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_format_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎞 MP4 (Video)", callback_data="format_mp4"),
            InlineKeyboardButton("🎧 MP3 (Audio)", callback_data="format_mp3")
        ]
    ])

def get_video_quality_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("360p", callback_data="video_360"),
            InlineKeyboardButton("480p", callback_data="video_480"),
        ],
        [
            InlineKeyboardButton("720p", callback_data="video_720"),
            InlineKeyboardButton("1080p", callback_data="video_1080"),
        ]
    ])

def get_audio_quality_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("128kbps", callback_data="audio_128"),
            InlineKeyboardButton("192kbps", callback_data="audio_192"),
            InlineKeyboardButton("320kbps", callback_data="audio_320"),
        ]
    ])

def get_delivery_type_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📤 Send as File", callback_data="as_file"),
            InlineKeyboardButton("🗂 Send as Document", callback_data="as_document")
        ]
    ])