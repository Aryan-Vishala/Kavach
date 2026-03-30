import json
import os

DB_PATH = "storage/db.json"


def load_db():
    if not os.path.exists(DB_PATH):
        return {"videos": []}

    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def add_video(video_data):
    db = load_db()
    db["videos"].append(video_data)
    save_db(db)