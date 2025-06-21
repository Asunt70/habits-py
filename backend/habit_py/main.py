"""main wrapper"""

import json
import argparse
from habit_py.setup import main as setup
from habit_py.track import main as track_habits
from habit_py.create_habit import main as create_habit
from habit_py.reset import main as reset
from config.config import CONFIG_PATH


def load_config():
    """loads config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


parser = argparse.ArgumentParser(description="Habit Tracker CLI")
subparsers = parser.add_subparsers(dest="command")
create_parser = subparsers.add_parser("create", help="Create a new habit")
create_parser.add_argument("habit_name", type=str, help="Name of the habit to create")
track_parser = subparsers.add_parser("track", help="Track habits")
reset_parser = subparsers.add_parser(
    "reset", help="Resets the habit tracker, WARNING: All data will be lost"
)
graph_parser = subparsers.add_parser("graph", help="Graph the habits ")
graph_parser.add_argument(
    choices=["lastweek", "week", "month", "year"],
    type=str,
    dest="graph_type",
    help="Type of graph to display",
)
args = parser.parse_args()


def main():
    """main function"""
    config = load_config()
    if config["first_run"] == "false":
        setup()
        # add a get started message
    if args.command == "track":
        track_habits()
        return
    if args.command == "reset":
        reset()
        print("please re-run habitpy setup")
        return
    if args.command == "create":
        create_habit(args.habit_name)
        return


if __name__ == "__main__":
    main()
