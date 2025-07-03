"""reset config.json and deletes database"""

import os
from habitpy.config.config import CONFIG_PATH, DATABASE_PATH
from habitpy.utils.functions import yes_no_prompt
from habitpy.export import main as export_habits


def main():
    """main function"""
    ask_reset = yes_no_prompt(
        "Are you sure you want to reset Habitpy? (y/n)\nWARNING THIS WILL DELETE ALL YOUR DATA\n=> "
    )
    if "y" not in ask_reset:
        print("Reset cancelled.")
        return
    export_habits(show=False)
    os.remove(DATABASE_PATH)
    print("removed user folder")
    os.remove(CONFIG_PATH)
    print("removed config.json")
    print("Habitpy has been reset, please run 'habitpy setup' to start again.")
