import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

MONGO_URI = os.environ.get("MONGO_URI", "")
DB_NAME = "youtube_bot"

DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL"))
ADMIN_USERS = list(map(int, os.environ.get("ADMIN_USERS", "").split(",")))