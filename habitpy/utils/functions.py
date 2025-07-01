"""global functions"""

import sqlite3 as db
import datetime
from habitpy.config.config import DATABASE_PATH


def yes_no_prompt(prompt):
    """A (y/n) input, only accepts y/n"""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["y", "n"]:
            return user_input
        print("please enter 'y' for yes or 'n' for no")


def float_input(prompt, stop: float | None = None):
    """A float input, only accepts floats"""
    while True:
        try:
            num = float(input(prompt))
            if stop is not None and num not in range(1, stop):
                print("enter valid number")
                continue
            return num
        except ValueError:
            print("please enter a number")


def int_input(prompt, stop: int | None = None):
    """An int input, only accepts integers"""
    while True:
        try:
            num = int(input(prompt))
            if stop is not None and num not in range(1, stop):
                print("enter valid number")
                continue
            return num
        except ValueError:
            print("please enter a number")


def multi_int_input(prompt):
    """An int input, accepts several integers seperated by spaces"""
    while True:
        user_input_str = input(prompt).strip()

        if not user_input_str:
            print("Input cannot be empty. Please enter numbers separated by spaces.")
            continue

        user_input_list = user_input_str.split(" ")
        valid_integers = []
        all_valid = True

        for i in user_input_list:
            if not i:
                continue
            if len(i) >= 2:
                print("enter valid numbers from 0-9 separated by space")
                break
            try:
                valid_integers.append(int(i))
            except ValueError:
                print("please enter only numbers")
                all_valid = False
                break

        if all_valid is True:
            return valid_integers


def get_habits():
    """get habits col from user_data table return a list"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habits FROM user_data")
            return cursor.fetchall()
    except db.Error as e:
        print(f"Database error: {e}")
        return []


def get_cols():
    """get cols from database returns a list"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habits")
            cols = [desc[0] for desc in cursor.description]
            return cols
    except db.Error as e:
        print(f"Database error: {e}")
        return None


def get_record():
    """gets today record returns a tuple"""
    try:
        with db.connect(
            database=DATABASE_PATH, detect_types=db.PARSE_DECLTYPES
        ) as conn:
            cursor = conn.cursor()
            today = datetime.date.today()
            cursor.execute("SELECT * from habits WHERE date = ?", (today,))
            return cursor.fetchall()
    except db.Error as e:
        print(f"Database Error: {e}")
        return None
