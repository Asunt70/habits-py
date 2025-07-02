"""adds a habit to habits column in user_data table"""

import sqlite3 as db
from habitpy.utils.functions import yes_no_prompt, get_habits
from habitpy.config.config import DATABASE_PATH


def create_habit(habit):
    """main function"""
    result = get_habits()
    if result and isinstance(result[0][0], str) and habit in result[0][0]:
        print(f"{habit} is already created")
        return
    confirm_habit = yes_no_prompt(f"are you sure to create {habit}? (y/n)\n=> ")
    if "y" in confirm_habit:
        add_habit = result[0] + (habit,)
        updated_response = ",".join(add_habit)
        try:
            with db.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE user_data
                    SET habits= ?
                    """,
                    (updated_response,),
                )
                conn.commit()
                print(f"{habit} habit added")
        except db.Error as e:
            print(f"Database error: {e}")


def delete_habit(habit: str):
    """main function"""
    result = get_habits()
    if result is None or not result:
        print("it seems like you don't have habits, reset or create one.")
        return
    if result and isinstance(result[0][0], str) and habit not in result[0][0]:
        print(f"{habit} doesn't exist try with another")
        return
    if len(result[0][0].split(",")) == 1:
        print(f"you can't leave no habits please create another to delete '{habit}'")
        return
    confirm_habit = yes_no_prompt(f"are you sure to delete {habit}? (y/n)\n=> ")
    if "y" in confirm_habit:
        habits = result[0][0].split(",")
        habits.remove(habit)
        habits = ",".join(habits)
        try:
            with db.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""UPDATE user_data SET habits = ?;""", (habits,))
                conn.commit()
        except db.Error as e:
            print(f"Database error: {e}")
        habits_columns = columns_names()
        if habit in habits_columns:
            try:
                with db.connect(database=DATABASE_PATH) as conn:
                    cur = conn.cursor()
                    cur.execute(f"ALTER TABLE habits DROP COLUMN {habit}")
                    conn.commit()
            except db.Error as e:
                print(f"Database error: {e}")
        print(f"{habit} habit deleted")


def show_habits():
    """shows habits to the user"""
    response = get_habits()
    if response is None or not response:
        print("it seems like you don't have habits, reset or create one.")
        return
    habits = response[0][0].split(",")
    print("your habits:")
    for i, col in enumerate(habits, start=1):
        print(f"{i}. {col}")


def columns_names():
    """loads all the columns names from habits table"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
        cur.execute("PRAGMA table_info(habits)")
        columns_info = cur.fetchall()
        column_names = [col[1] for col in columns_info]
        return column_names
    except db.Error as e:
        print(f"Database error: {e}")
        return None
