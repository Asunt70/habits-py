"""Returns a cheer to display while tracking habits"""

import json
import sqlite3 as db
import random
from habitpy.config.config import CONFIG_PATH, DATABASE_PATH


def load_config():
    """loads config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def get_cheers():
    """loads cheers from database"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT cheers FROM user_data")
            response = cur.fetchone()
            return response
    except db.Error as e:
        print(f"Database error: {e}")
        return None


def main():
    """loads cheers from database and returns a random one"""
    config = load_config()
    if config["cheers"] == "true":
        response = get_cheers()
        if response:
            cheers = response[0].split(",")
            len_cheers = len(cheers)
            if len_cheers > 1:
                ran_num = random.randint(0, len_cheers - 1)
                print(cheers[ran_num])
                return
            print(cheers[0])
            return
    return None
