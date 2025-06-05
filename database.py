from pymongo import MongoClient
import os

# Load from environment variables or use default MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# Database and collection
db = client["yt_downloader_bot"]
users_collection = db["users"]

def add_user(user_id, username=None, first_name=None):
    if not users_collection.find_one({"_id": user_id}):
        users_collection.insert_one({
            "_id": user_id,
            "username": username,
            "first_name": first_name
        })

def count_users():
    return users_collection.count_documents({})

def get_all_users():
    return users_collection.find({})