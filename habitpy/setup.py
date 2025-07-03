"""setup"""

import sqlite3 as db
import json
import os
from habitpy.utils.functions import yes_no_prompt, multi_int_input
from habitpy.config.config import CONFIG_PATH, DATABASE_PATH


def load_config():
    """loads config.json"""
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
            json.dump(
                {"first_run": "true", "cheers": "false"},
                config_file,
                indent=4,
            )
    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def create_cheers():
    """create motivational messages for the user"""
    while True:
        ask_cheer = yes_no_prompt(
            "Do you want to set motivational messages to cheer you while interacting with the app? (y/n)\n=> "
        )
        if "y" in ask_cheer:
            get_cheers = str(
                input(
                    "use ',' followed by a SPACE to separate them\n example: you can!, i can!, i'm the best!\n=>"
                )
            )
            confirm_cheers = yes_no_prompt(
                f"are you sure to create ({get_cheers})? (y/n)\n=> "
            )
            if "y" in confirm_cheers:
                return get_cheers.split(", ")
            print("Okay, we will re-run previous commands!")
            continue
        print(
            "there won't be any cheers\nyou can add them later with 'habitpy setup cheers'"
        )
        return None


user_habits = []


def choose_habits():
    """choose habits for the user"""
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
    print("You can choose habits from the following list template:")
    for i, habit_template in enumerate(habits_template, start=1):
        print(f"{i}: {habit_template}")
    print("0: all of them\n9: skip")

    while True:
        chosen_habits = multi_int_input("=> ")
        for choice in chosen_habits:
            if choice == 0:
                print("All habits template selected")
                return user_habits.extend(habits_template)
            if choice in habit_map:
                key = habit_map[choice]
                if key in user_habits:
                    print(
                        f"Option: '{key}' already selected please enter valid options"
                    )
                    continue
                user_habits.append(key)
                if len(user_habits) == len(chosen_habits):
                    return user_habits
            elif choice == 9:
                print(
                    "skipped; REMEMBER to create your habits later with 'habitpy create habit_name'"
                )
                return


def main():
    """main function"""
    user_cheers = create_cheers()
    if not user_cheers is None:
        user_cheers = ",".join(user_cheers)
        config = load_config()
        config["cheers"] = "true"
        with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4)
    choose_habits()
    user_habits_string = ",".join(user_habits)

    try:
        with db.connect(DATABASE_PATH) as conn:
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
            "INSERT INTO user_data (cheers, habits) VALUES (?, ?)",
            (
                user_cheers,
                user_habits_string,
            ),
        )
        conn.commit()

    except db.Error as e:
        print(f"Database error: {e}")

    config = load_config()
    config["first_run"] = "true"
    with open(CONFIG_PATH, "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, indent=4)
    print("setup completed run 'habitpy -h' to see all available commands!")
