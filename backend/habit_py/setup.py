"""#todo"""

import sqlite3
import json
import os
from habit_py.utils.functions import yes_no_prompt, multi_int_input
from config.config import CONFIG_PATH, USER_FOLDER_PATH

if not os.path.exists(USER_FOLDER_PATH):
    os.makedirs(USER_FOLDER_PATH)


def load_config():
    """loads config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def create_cheers():
    """create motivational messages for the user"""
    while True:
        ask_cheer = yes_no_prompt(
            "Do you want to set motivational messages to cheer you while interacting with the app? (y/n)\n=> ",
        )
        if "y" in ask_cheer:
            get_cheers = str(
                input(
                    "use ',' followed by a SPACE to separate them\n example: you can!, i can!, i'm the best!\n=>"
                )
            )
            confirm_cheers = yes_no_prompt(
                f"are you sure to create {get_cheers}? (y/n)\n=> "
            )
            if "y" in confirm_cheers:
                return get_cheers.split(", ")
            print("Okay, we will re-run previous commands!")
            continue
        return print(
            "there won't be any cheers\nyou can add them later with 'habitpy setup cheers'"
        )


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
    chosen_habits = multi_int_input("=> ")

    for choice in chosen_habits:
        if choice == 0:
            print("all selected")
            user_habits.extend(habits_template)
        elif choice in habit_map:
            key = habit_map[choice]
            user_habits.append(key)

        elif choice == 9:
            print(
                "skipped; REMEMBER to create your habits later with 'habitpy create habit_name'"
            )

        else:
            print("please enter a correct value")
            break


def main():
    """main function"""
    user_name = str(input("How should i call you?\n=> "))
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
