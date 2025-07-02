"""main wrapper"""

import argparse
import os
from habitpy.setup import main as setup
from habitpy.track import main as track_habits
from habitpy.manage_habits import create_habit, delete_habit, show_habits
from habitpy.graphs_data import month_data, year_data, week_data
from habitpy.export import main as export_habits
from habitpy.reset import main as reset
from habitpy.config.config import CONFIG_PATH

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
export_parser = subparsers.add_parser("export", help="Export habits to a CSV file")
setup_parser = subparsers.add_parser("setup", help="Setup the habit tracker")
show_parser = subparsers.add_parser("show", help="Show your habits")
delete_parser = subparsers.add_parser("delete", help="Delete a habit")
delete_parser.add_argument("habit_name", type=str, help="Name of the habit to delete")

args = parser.parse_args()


def main():
    """main function"""
    if not os.path.exists(CONFIG_PATH):
        print("please run 'habitpy setup to use the app'")
        if args.command == "setup":
            setup()
    if os.path.exists(CONFIG_PATH):
        if args.command == "track":
            track_habits()
        if args.command == "reset":
            reset()
        if args.command == "create":
            create_habit(args.habit_name)
        if args.command == "graph":
            if args.data_format == "week":
                week_data(args.week_option)
            if args.data_format == "month":
                month_data(args.month_name)
            if args.data_format == "year":
                year_data(args.year)
        if args.command == "export":
            export_habits(show=True)
        if args.command == "setup":
            print("you already setup the app if you wanna reset run 'habitpy reset'")
        if args.command == "show":
            show_habits()
        if args.command == "delete":
            delete_habit(args.habit_name)


if __name__ == "__main__":
    main()
