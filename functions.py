"""global functions"""

import sqlite3
from config import DATABASE_PATH


def yes_no_prompt(prompt):
    """A (y/n) input, only accepts y/n"""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["y", "n"]:
            return user_input
        else:
            print("please enter 'y' for yes or 'n' for no")


def int_input(prompt):
    """An int input, only accepts integers"""
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
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
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habits FROM user_data")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
