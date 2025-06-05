def get_format_buttons():
    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("MP4", callback_data="format_mp4"),
         InlineKeyboardButton("MP3", callback_data="format_mp3")]
    ])

def get_delivery_type_buttons():
    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("As File", callback_data="as_file"),
         InlineKeyboardButton("As Document", callback_data="as_document")]
    ])