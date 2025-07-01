"""reset config.json and deletes database"""

import os
from config.config import CONFIG_PATH, DATABASE_PATH


def main():
    """main function"""
    os.remove(DATABASE_PATH)
    os.rmdir("user")
    print("removed user folder")
    os.remove(CONFIG_PATH)
    print("removed config.json")
