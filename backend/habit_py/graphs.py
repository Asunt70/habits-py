"""
This module provides utility functions for database manipulation.
"""

import sqlite3
import os
import webbrowser
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from habit_py.track import get_cols
from habit_py.utils.functions import int_input
from config.config import DATABASE_PATH

cols2 = get_cols()


def smart_num(x):
    """converts num into int if possible, else float"""
    if x == int(x):  # if x has no decimal part
        return int(x)
    return float(x)


def habits_average():
    """calculate the average of all the habits"""
    response = []

    try:
        for col in cols2[2:]:
            with sqlite3.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT {col} from habits")
                res = cursor.fetchall()
                response.append(res)
    except sqlite3.Error as e:
        print(f"Database Error {e}")
    formatted_response = [
        [item for tup in sublist for item in tup] for sublist in response
    ]
    nums = []
    for i in formatted_response:
        i = np.mean(i)
        nums.append(smart_num(i))
    average_dict = dict(zip(cols2[2:], nums))

    for i, (key, value) in enumerate(average_dict.items(), start=1):
        print(f"{i}. {key}: {value}")


def load_week(param):
    """load week data from database"""
    if param == 1:
        param = """
                SELECT
                    CASE strftime('%u', date)
                        WHEN '1' THEN 'Monday'
                        WHEN '2' THEN 'Tuesday'
                        WHEN '3' THEN 'Wednesday'
                        WHEN '4' THEN 'Thursday'
                        WHEN '5' THEN 'Friday'
                        WHEN '6' THEN 'Saturday'
                        WHEN '7' THEN 'Sunday'
                    END AS day_name,
                *
                FROM habits
                WHERE date >= date('now', 'weekday 0', '-6 days')
                AND date <= date('now', 'weekday 0');
            """
    else:
        param = """
                SELECT
                    CASE strftime('%u', date)
                        WHEN '1' THEN 'Monday'
                        WHEN '2' THEN 'Tuesday'
                        WHEN '3' THEN 'Wednesday'
                        WHEN '4' THEN 'Thursday'
                        WHEN '5' THEN 'Friday'
                        WHEN '6' THEN 'Saturday'
                        WHEN '7' THEN 'Sunday'
                    END AS day_name,
                *
                FROM habits
                WHERE date >= date('now', 'weekday 0', '-13 days')
                AND date <= date('now', 'weekday 0', '-7 days');
            """
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(param)
            cols = [desc[0] for desc in cur.description]
            response = cur.fetchall()
            return cols, response
    except sqlite3.Error as e:
        print(f"Database Error as {e}")


def draw_week(df, habit, num):
    """draws the week graph"""
    if num == 1:
        title_txt = "This Week"
    else:
        title_txt = "Last Week"
    df.plot(x="day_name", y=[habit], kind="bar", title=title_txt, figsize=(5, 8))
    x = df[habit].mean()
    plt.axhline(y=x, color="gray", label="Average", linestyle="--")
    plt.xticks(rotation=0, ha="center")
    plt.xlabel("")
    FILE = "assets/myfig.png"
    plt.savefig(FILE)
    webbrowser.open("file://" + os.path.abspath(FILE))


def user_input(param):
    "gets int input"
    for i, col in enumerate(param, start=1):
        print(f"{i}. {col}")
    sel_option = int_input("==> ", len(param) + 1)
    return param[sel_option - 1]


def week_graph():
    """simple menu to see week graphs"""
    last_or_current = int_input(prompt="1. Current Week\n2. Last Week\n => ", stop=3)
    cols, res = load_week(last_or_current)
    df = pd.DataFrame(res)
    df.columns = cols
    habits = cols[2:]

    habit_to_track = user_input(habits)
    draw_week(df, habit_to_track, last_or_current)


def load_month():
    "loads the available months from the year"
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT DISTINCT strftime('%m', date) as month
                FROM habits
                WHERE strftime('%Y', date) = strftime('%Y', 'now')
                ORDER BY month DESC
                """
            )
            response = cur.fetchall()
            return response
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return None


def get_month(month):
    """get data from month"""
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur_year = datetime.now().strftime("%Y")
            cur.execute(
                """
                SELECT *
                FROM habits
                WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
                ORDER BY date;
            """,
                (cur_year, month),
            )
            res = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            return col_names, res
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return None


def month_graph():
    """intended to show a graph of the selected month"""
    response = load_month()
    if response == [] or response is None:
        print("empty months try with another")
        return
    months = []
    for tp in response:
        months.append(tp[0])
    print("select option")
    dates = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    for i, month in enumerate(months, start=1):
        print(f"{i}. {dates.get(month)}")
    sel_month = int_input("=> ", stop=len(months) + 1)
    cols, res = get_month(months[sel_month - 1])
    df = pd.DataFrame(res)
    df.columns = cols
    habits = cols[2:]
    habit_to_graph = user_input(habits)
    print(df)


def load_years():
    """loads year"""
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            query = """SELECT DISTINCT substr(date, 1, 4) AS year
                        FROM habits
                        ORDER BY year DESC;"""
            cur.execute(query)
            res = cur.fetchall()

            return res
    except sqlite3.Error as e:
        print(f"Database Error {e}")


def select_year(year):
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM habits WHERE strftime('%Y', date) = ?;", (str(year),)
            )
            res = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            return col_names, res
    except sqlite3.Error as e:
        print(f"Database Error {e}")


def draw_year(dataframe, habit):
    """BETAAAA"""
    dataframe.plot(x="date", y=[habit], kind="scatter", title=2, figsize=(5, 8))
    x = dataframe[habit].mean()
    plt.axhline(y=x, color="gray", label="Average", linestyle="--")
    plt.xticks(rotation=0, ha="center")
    plt.xlabel("")
    FILE = "assets/myfig.png"
    plt.savefig(FILE)
    webbrowser.open("file://" + os.path.abspath(FILE))


def year_graph():
    response = load_years()
    years = []
    for tp in response:
        years.append(tp[0])
    print("Select option")
    for i, year in enumerate(years, start=1):
        print(f"{i}. {year}")
    got_year = int_input("=> ", stop=len(years) + 1)
    cols, res = select_year(years[got_year - 1])
    if res == []:
        print("empty year try with another")
        return
    df = pd.DataFrame(res)
    df.columns = cols
    habits = cols[2:]
    habit_to_graph = user_input(habits)
    draw_year(df, habit_to_graph)


def habit_graph():
    """simple menu to see habit graphs"""
    # selected menu in habit graph menu
    sel_menu = int_input("1. Week\n2. Month\n3. Year\n==> ")
    if sel_menu == 1:
        week_graph()
    elif sel_menu == 2:
        print("month")
    elif sel_menu == 3:
        load_years()
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


month_graph()
