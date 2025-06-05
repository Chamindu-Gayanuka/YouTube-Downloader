from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['yt_bot']

def add_user(user_id, username, first_name):
    db.users.update_one(
        {"_id": user_id},
        {"$set": {"username": username, "first_name": first_name}},
        upsert=True
    )

def get_all_users():
    return list(db.users.find())

def count_users():
    return db.users.count_documents({})