"""
This module provides utility functions for database manipulation.
"""

import sqlite3
from datetime import datetime
import pandas as pd
import numpy as np
from track import get_cols
from utils.functions import int_input
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
        return None


def user_input(param):
    "gets int input"
    print("Select an option")
    for i, col in enumerate(param, start=1):
        print(f"{i}. {col}")
    sel_option = int_input("==> ", len(param) + 1)
    return param[sel_option - 1]


def week_data():
    """simple menu to see week graphs"""
    last_or_current = int_input(prompt="1. Current Week\n2. Last Week\n => ", stop=3)
    cols, response = load_week(last_or_current)
    if response == [] or response is None:
        return
    df = pd.DataFrame(response)
    df.columns = cols
    return df


def load_month(month):
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


def get_month_data(habit: str, month: str):
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur_year = datetime.now().strftime("%Y")
            cur.execute(
                f"""SELECT date,{habit} FROM habits  WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
                ORDER BY date;""",
                (cur_year, month),
            )
            res = cur.fetchall()
            return res
    except sqlite3.Error as e:
        print(f"Database Error {e}")


# args list months etc.
def month_data(month_to_get: str):
    """intended to show a graph of the selected month"""
    dates = {
        "january": "01",
        "february": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12",
    }
    formatted_month = dates.get(month_to_get)
    cols, response = load_month(formatted_month)
    if response is None or response == []:
        print("no data for specified month")
        return
    habits = cols[2:]
    habit_to_track = user_input(habits)
    data = get_month_data(habit_to_track, formatted_month)
    df = pd.DataFrame(data)
    df.columns = ["Date", habit_to_track]
    return df


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
        return None


def get_year_data(year):
    """gets all the specified data from habits"""
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


def year_data(year_to_get):
    """returns data from the year"""
    response = load_years()
    if response == [] or response is None:
        print("empty months try with another")
        return
    years = []
    for tp in response:
        years.append(tp[0])
    # print("Select option")
    # for i, year in enumerate(years, start=1):
    #     print(f"{i}. {year}")
    # got_year = int_input("=> ", stop=len(years) + 1)
    cols, res = get_year_data(year_to_get)
    if res == []:
        print("empty year try with another")
        return
    df = pd.DataFrame(res)
    df.columns = cols
    return df


# def main(graph_type):
#     """main function for graphing habits"""
#     if graph_type == "week":
#         return week_graph()
#     elif graph_type == "month":
#         return month_graph()
#     elif graph_type == "year":
#         return year_graph(year_to_graph)
#     else:
#         print("please enter a valid option")
#         return
