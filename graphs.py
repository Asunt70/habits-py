"""
This module provides utility functions for database manipulation.
"""

import sqlite3
import os
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from track_habits import get_cols
from functions import int_input
from config import DATABASE_PATH

cols = get_cols()
# try:
#     with sqlite3.connect(database=DATABASE_PATH) as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * from habits")
#         results = cursor.fetchall()
#         df = pd.DataFrame(results)
# except sqlite3.Error as e:
#     print(f"Database Error {e}")

# df.columns = cols
# x = df["water"].mean()
# print(x)
# df.plot(x="date", y=["weight"], kind="bar", title="Graph", figsize=(18, 10))
# plt.axhline(y=x, color="gray", label="Average")
# FILE = "assets/myfig.png"

# plt.savefig(FILE)
# webbrowser.open("file://" + os.path.abspath(FILE))

# df = df.to_string(index=False)


def smart_num(x):
    """converts num into int if possible else float"""
    if x == int(x):  # if x has no decimal part
        return int(x)
    return float(x)


def habits_average():
    """calculate the average of all the habits"""
    response_list = []

    try:
        for col in cols[2:]:
            with sqlite3.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT {col} from habits")
                response = cursor.fetchall()
                response_list.append(response)
    except sqlite3.Error as e:
        print(f"Database Error {e}")
    formatted_response = [
        [item for tup in sublist for item in tup] for sublist in response_list
    ]
    nums = []
    for i in formatted_response:
        i = np.mean(i)
        nums.append(smart_num(i))
    average_dict = dict(zip(cols[2:], nums))

    for i, (key, value) in enumerate(average_dict.items(), start=1):
        print(f"{i}. {key}: {value}")


def load_week(param):
    if param == 1:
        param = """
                SELECT *
                FROM habits
                WHERE date >= date('now', 'weekday 0', '-6 days')
                AND date <= date('now', 'weekday 0');
            """
    if param == 2:
        param = """
                SELECT *
                FROM habits
                WHERE date >= date('now', 'weekday 0', '-13 days')
                AND date <= date('now', 'weekday 0', '-7 days');
            """
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(param)
            response = cursor.fetchall()
            return response
    except sqlite3.Error as e:
        print(f"Database Error as {e}")


def draw_week(df, habit):
    df.plot(x="date", y=[habit], kind="bar", title="This week", figsize=(5, 8))
    x = df[habit].mean()
    plt.axhline(y=x, color="gray", label="Average")
    FILE = "assets/myfig.png"
    plt.savefig(FILE)
    webbrowser.open("file://" + os.path.abspath(FILE))


def last_or_current():
    while True:
        if 1 <= last_or_current <= 2:
            return
        continue


def week_graph():
    last_or_current = int_input(prompt="1. Current Week\n2. Last Week\n => ", stop=3)

    df = pd.DataFrame(load_week(last_or_current))
    df.columns = cols
    habits = cols[2:]

    def user_input():
        for i, col in enumerate(habits, start=1):
            print(f"{i}. {col}")
        sel_option = int_input("==> ", len(habits) + 1)
        return habits[sel_option - 1]

    habit_to_track = user_input()
    draw_week(df, habit_to_track)


def habit_graph():
    """simple menu to see habit graphs"""
    # selected menu in habit graph menu
    sel_menu = int_input("1. Week\n2. Month\n3. Year\n==> ")
    if sel_menu == 1:
        week_graph()
    elif sel_menu == 2:
        print("month")
    elif sel_menu == 3:
        print("year")
    else:
        print("please enter a valid option")


def main():
    """main function"""
    # selected 1st menu
    sel_menu = int_input("1. Habit Graph\n2. Average\n==> ")
    if sel_menu == 1:
        habit_graph()
    if sel_menu == 2:
        habits_average()


week_graph()
