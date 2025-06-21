"""adds a habit to habits column in user_data table"""

import sqlite3
from habit_py.utils.functions import yes_no_prompt, get_habits
from config.config import DATABASE_PATH


def main(habit):
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
            with sqlite3.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE user_data
                    SET habits= ?
                    """,
                    (updated_response,),
                )
                conn.commit()
                print(f"{habit} added successfully")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
