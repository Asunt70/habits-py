import sqlite3, json, os
from functions import yes_no_prompt, multi_int_input

user_folder_path = "user"
if not os.path.exists("user"):
    os.makedirs(user_folder_path)

# update first_run_flag
path_config = "config.json"
if not os.path.exists(path_config):
    config_dict = {"first_run": "false"}
    with open(path_config, "w") as f:
        json.dump(config_dict, f)


def load_config():
    with open(path_config, "r") as f:
        return json.load(f)


# metadata
def load_metadata():
    with open("metadata.json", "r") as f:
        return json.load(f)


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
    while True:
        ask_cheer = yes_no_prompt(f"{m_ask_cheer}")
        if "y" in ask_cheer:
            get_cheers = str(input(f"{m_get_cheers}"))
            confirm_cheers = yes_no_prompt(f"{m_confirm_cheers}")
            if "y" in confirm_cheers:
                return get_cheers.split(", ")
            else:
                print("Okay, we will re-run previous commands!")
        else:
            print(f"{m_no_cheers}")
            return


user_habits = []


def choose_habits():
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
    with open(path_config, "w") as f:
        json.dump(config, f, indent=4)
