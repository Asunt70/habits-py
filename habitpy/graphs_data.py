"""
This module provides graphing functionality for habit tracking data.
"""

import sqlite3 as db
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from habitpy.utils.functions import int_input
from habitpy.config.config import DATABASE_PATH


# if habits length is less than 2 not display select option
def user_input(param):
    "gets int input"
    print("Select an option")
    for i, col in enumerate(param, start=1):
        print(f"{i}. {col}")
    sel_option = int_input("==> ", len(param) + 1)
    return param[sel_option - 1]


def load_week(param):
    """load week data from database"""
    if param == "current":
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
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(param)
            cols = [desc[0] for desc in cur.description]
            response = cur.fetchall()
            return cols, response
    except db.Error as e:
        print(f"Database Error as {e}")
        return None


def get_week_data(habit, param):
    """load week data from database"""
    if param == "current":
        param = f"""
                SELECT
                    CASE strftime('%u', date)
                        WHEN '1' THEN 'Monday'
                        WHEN '2' THEN 'Tuesday'
                        WHEN '3' THEN 'Wednesday'
                        WHEN '4' THEN 'Thursday'
                        WHEN '5' THEN 'Friday'
                        WHEN '6' THEN 'Saturday'
                        WHEN '7' THEN 'Sunday'
                    END AS Day,
                {habit}
                FROM habits
                WHERE date >= date('now', 'weekday 0', '-6 days')
                AND date <= date('now', 'weekday 0');
            """
    else:
        param = f"""
                SELECT
                    CASE strftime('%u', date)
                        WHEN '1' THEN 'Monday'
                        WHEN '2' THEN 'Tuesday'
                        WHEN '3' THEN 'Wednesday'
                        WHEN '4' THEN 'Thursday'
                        WHEN '5' THEN 'Friday'
                        WHEN '6' THEN 'Saturday'
                        WHEN '7' THEN 'Sunday'
                    END AS Day,
                {habit}
                FROM habits
                WHERE date >= date('now', 'weekday 0', '-13 days')
                AND date <= date('now', 'weekday 0', '-7 days');
            """
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(param)
            response = cur.fetchall()
            return response
    except db.Error as e:
        print(f"Database Error as {e}")
        return None


def week_data(last_or_current: str):
    """simple menu to see week graphs"""
    cols, response = load_week(last_or_current)
    if response == [] or response is None:
        print("week is empty, no data will be shown")
        return None
    habits = cols[3:]
    habit_to_track = user_input(habits)
    data = get_week_data(habit_to_track, last_or_current)
    if data is None:
        print("An error has occured... please try again")
        return None
    df = pd.DataFrame(data)
    df.columns = ("Day", habit_to_track)
    avg = df[habit_to_track].mean()
    fig = go.Figure(
        data=[
            go.Bar(
                x=df["Day"],
                y=df[habit_to_track],
                marker_color="dodgerblue",
            )
        ],
        layout=dict(barcornerradius=15),
    )
    fig.update_layout(template="plotly_dark")
    fig.update_layout(title=f"{habit_to_track} for the {last_or_current} week")
    fig.add_shape(
        type="line",
        x0=0,
        x1=1,
        y0=avg,
        y1=avg,
        line=dict(
            color="lightgray",
            width=2,
            dash="dash",
        ),
        xref="paper",
        yref="y",
    )
    fig.show()


def load_month(month):
    """loads the available habits for the specified month"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
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
    except db.Error as e:
        print(f"Database Error {e}")
        return None


def get_month_data(habit: str, month: str):
    """get the month data for the specified habit"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur_year = datetime.now().strftime("%Y")
            cur.execute(
                f"""SELECT date,{habit} FROM habits
                WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
                ORDER BY date;""",
                (cur_year, month),
            )
            res = cur.fetchall()
            return res
    except db.Error as e:
        print(f"Database Error {e}")
        return None


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
        print("month is empty, no data will be shown")
        return None
    habits = cols[2:]
    habit_to_track = user_input(habits)
    data = get_month_data(habit_to_track, formatted_month)
    if data is None:
        print("An error occurred... please try again")
        return None
    df = pd.DataFrame(data)
    df.columns = ["date", habit_to_track]
    avg = df[habit_to_track].mean()
    fig = go.Figure(
        data=[
            go.Scatter(x=df["date"], y=df[habit_to_track], marker_color="dodgerblue")
        ],
        layout=dict(barcornerradius=15),
    )
    fig.update_layout(template="plotly_dark")
    fig.update_layout(title=f"{habit_to_track} for {month_to_get.capitalize()}")
    fig.add_shape(
        type="line",
        x0=0,
        x1=1,
        y0=avg,
        y1=avg,
        line=dict(
            color="lightgray",
            width=2,
            dash="dash",
        ),
        xref="paper",
        yref="y",
    )
    fig.show()


def load_year(year):
    """gets all the data from the specified year"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM habits WHERE strftime('%Y', date) = ?;",
                (str(year),),
            )
            res = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            return col_names, res
    except db.Error as e:
        print(f"Database Error {e}")
        return None


def get_year_data(habit, year):
    """gets all the data for the specified habit in the specified year"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT date,{habit} FROM habits WHERE strftime('%Y', date) = ?;",
                (str(year),),
            )
            res = cur.fetchall()
            return res
    except db.Error as e:
        print(f"Database Error {e}")
        return None


def year_data(year: int):
    """returns data from the year"""
    cols, response = load_year(year)
    if response == [] or response is None:
        print("year is empty, no data will be shown")
        return None
    habits = cols[2:]
    habit_to_track = user_input(habits)
    data = get_year_data(habit_to_track, year)
    if data is None:
        print("An error occurred... please try again")
        return None
    df = pd.DataFrame(data)
    df.columns = ["date", habit_to_track]
    avg = df[habit_to_track].mean()
    fig = go.Figure(
        data=[
            go.Scatter(x=df["date"], y=df[habit_to_track], marker_color="dodgerblue")
        ],
        layout=dict(barcornerradius=15),
    )
    fig.update_layout(template="plotly_dark")
    fig.update_layout(title=f"{habit_to_track} for {year}")
    fig.add_shape(
        type="line",
        x0=0,
        x1=1,
        y0=avg,
        y1=avg,
        line=dict(
            color="lightgray",
            width=2,
            dash="dash",
        ),
        xref="paper",
        yref="y",
    )
    fig.show()
