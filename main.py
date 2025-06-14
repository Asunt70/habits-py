"""main wrapper"""

import json
from first_run import main as first_run
from track_habits import main as track_habits
from create_habit import main as create_habit
from reset import main as reset
from functions import int_input
from config import CONFIG_PATH, METADATA_PATH


def load_metadata():
    """loads metadata"""
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


meta = load_metadata()
m_menu = meta["menus"]["principal"]


def load_config():
    """loads config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """main function"""
    config = load_config()
    if config["first_run"] == "false":
        first_run()
    while True:
        selected_option = int_input(m_menu)
        if selected_option == 1:
            track_habits()
            continue
        if selected_option == 2:
            create_habit()
            continue
        if selected_option == 5:
            reset()
            print("please re-run to setup")
            break
        if selected_option == 0:
            break


main()
