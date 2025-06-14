"""reset config.json and deletes database"""

import os
import json


def main():
    """main function"""
    os.remove("user/user_data.db")
    os.rmdir("user")
    print("succesfully removed user folder")
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    config["first_run"] = "false"
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    print("succesfully updated config.json")
