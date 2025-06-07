import sqlite3
from functions import yes_no_prompt
database_path = 'user/user_data.db'
def get_habits():
    try:
        with sqlite3.connect(database=database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habits FROM user_data")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f'Database error: {e}')
        return []
            
def main():
    habit = str(input('please provide the name of the habit\n==> '))
    confirm_habit = yes_no_prompt(f'create {habit}? (y/n)\n==> ')
    if 'y' in confirm_habit:
        result = get_habits()
        print(result)
        updated_result = result[0] + (habit,)
        res = ','.join(updated_result)
        # try:
        #     with sqlite3.connect(database=database_path) as conn:
        #         cursor = conn.cursor()
        #         cursor.execute ("""
        #             UPDATE user_data
        #             SET habits= (?)
        #             """, (res,)
        #             )
        #         conn.commit()
        #         print(f'{habit} successfully added')
        # except sqlite3.Error as e:
        #     print(f'Database error: {e}')


    



