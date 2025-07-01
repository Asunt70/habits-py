"""main wrapper"""

import json
import argparse

from setup import main as setup
from track import main as track_habits
from create_habit import main as create_habit
from graphs_data import month_data, year_data, week_data
from reset import main as reset
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
graph_parser = graph_parser.add_subparsers(dest="data_format", required=True)
week_graph = graph_parser.add_parser(
    "week", help="Graph habits from current week or last week"
)
month_graph = graph_parser.add_parser("month", help="Graph habits from specific month")
year_graph = graph_parser.add_parser("year", help="Graph habits from specific year")
week_graph.add_argument(
    choices=["current", "last"],
    dest="week_option",
    type=str,
    help="Select current or last week",
)
month_graph.add_argument(
    choices=[
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ],
    dest="month_name",
    type=str,
    help="Select a month to graph",
)
year_graph.add_argument("year", type=int, help="Select a year to graph")
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
    if args.command == "graph":
        if args.data_format == "week":
            week_data(args.week_option)
        if args.data_format == "month":
            month_data(args.month_name)
            return
        if args.data_format == "year":
            year_data(args.year)


if __name__ == "__main__":
    main()
