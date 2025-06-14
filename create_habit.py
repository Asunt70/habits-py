"""adds a habit to habits column in user_data table"""

import sqlite3
from functions import yes_no_prompt, get_habits
from config import DATABASE_PATH


def main():
    """main function"""
    habit = str(input("please provide the name of the habit\n==> "))
    result = get_habits()
    if habit in result[0][0]:
        print(f"{habit} habit is already created")
    else:
        confirm_habit = yes_no_prompt(f"create {habit}? (y/n)\n==> ")
        if "y" in confirm_habit:
            result = get_habits()
            updated_result = result[0] + (habit,)
            res = ",".join(updated_result)
            try:
                with sqlite3.connect(database=DATABASE_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        UPDATE user_data
                        SET habits= (?)
                        """,
                        (res,),
                    )
                    conn.commit()
                    print(f"{habit} successfully added")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
