from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["discord_bot"]
events_collection = db["events"]

def add_event(title, date, description, location):
    event = {
        "title": title,
        "date": date,
        "description": description,
        "location": location
    }
    events_collection.insert_one(event)

def remove_event(title):
    result = events_collection.delete_one({"title": title})
    return result.deleted_count > 0

def list_events():
    events = events_collection.find()
    formatted = []
    for e in events:
        formatted.append(f"{e['title']} — {e['date']} in {e['time']}\n{e['description']}\n at  {e['location']}")
    return "\n".join(formatted) if formatted else "no eveent find ."
