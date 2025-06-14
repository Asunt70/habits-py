"""#todo"""

# try to put load functions in functions.py
import sqlite3
import json
import os
from functions import yes_no_prompt, multi_int_input
from config import CONFIG_PATH, METADATA_PATH, USER_FOLDER_PATH

if not os.path.exists(USER_FOLDER_PATH):
    os.makedirs(USER_FOLDER_PATH)

# update first_run_flag
if not os.path.exists(CONFIG_PATH):
    config_dict = {"first_run": "false"}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_dict, f)


def load_config():
    """loads config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


# metadata
def load_metadata():
    """loads metadata"""
    with open(METADATA_PATH, "r", encoding="utf-8") as meta_file:
        return json.load(meta_file)


meta = load_metadata()
m_choose_habits = meta["choose_habits"]
m_welcome = meta["first_run"]["welcome"]
m_ask_name = meta["first_run"]["ask_name"]
m_ask_cheer = meta["first_run"]["ask_cheer"]
m_get_cheers = meta["first_run"]["ask_cheers"]
m_invalid_option = meta["errors"]["invalid_option"]
m_no_cheers = meta["first_run"]["no_cheers"]
m_confirm_cheers = meta["first_run"]["confirm_cheers"]


def create_cheers():
    """#todo"""
    while True:
        ask_cheer = yes_no_prompt(f"{m_ask_cheer}")
        if "y" in ask_cheer:
            get_cheers = str(input(f"{m_get_cheers}"))
            confirm_cheers = yes_no_prompt(f"{m_confirm_cheers}")
            if "y" in confirm_cheers:
                return get_cheers.split(", ")
            print("Okay, we will re-run previous commands!")
            continue
        return print(f"{m_no_cheers}")


user_habits = []


def choose_habits():
    """#todo"""
    chosen_habits = multi_int_input(f"{m_choose_habits}")
    habits_template = (
        "water",
        "weight",
        "exercise",
        "meditation",
        "study",
        "reading",
        "mod",
    )
    habit_map = {
        1: "water",
        2: "weight",
        3: "exercise",
        4: "meditation",
        5: "reading",
        6: "study",
        7: "mod",
    }
    for choice in chosen_habits:
        if choice == 0:
            print("all selected")
            user_habits.extend(habits_template)
        elif choice in habit_map:
            key = habit_map[choice]
            user_habits.append(key)

        elif choice == 9:
            break

        else:
            print("please enter a correct value")
            break


def main():
    """main function"""
    user_name = str(input(m_ask_name))
    user_cheers = create_cheers()
    if not user_cheers is None:
        user_cheers = ",".join(user_cheers)
    choose_habits()
    user_habits_string = ",".join(user_habits)

    try:
        with sqlite3.connect("user/user_data.db") as conn:
            cursor = conn.cursor()
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS user_data (
                name TEXT,
                cheers TEXT,
                habits TEXT
                );
                CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE
                );
            """
            )
        cursor.execute(
            "INSERT INTO user_data (name, cheers, habits) VALUES (?, ?, ?)",
            (
                user_name,
                user_cheers,
                user_habits_string,
            ),
        )
        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    config = load_config()
    config["first_run"] = "true"
    with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, indent=4)
