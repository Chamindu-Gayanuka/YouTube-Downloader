import os
from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

MONGO_URI = os.getenv("MONGO_URI", "")
DUMP_CHANNEL = int(os.getenv("DUMP_CHANNEL", ""))
ADMIN_USERS = int(os.getenv("ADMIN_USERS", ""))