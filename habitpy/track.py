"""track habits"""

# ALLOW FLOAT
import datetime
import sqlite3 as db

import habitpy.utils.date_adapter as date_adapter
from habitpy.config.config import DATABASE_PATH
from habitpy.utils.cheers import main as cheers
from habitpy.utils.functions import float_input, get_habits, get_record

cols = []


# get the cols from the database
def get_cols():
    """get cols from database returns a list"""
    cols.clear()
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            data = cursor.execute(
                """
                SELECT * FROM habits
            """
            )
            for column in data.description:
                cols.append(column[0])
            return cols
    except db.Error as e:
        print(f"Database error: {e}")
        return None


def check_cols():
    """check if there are differences between the habit table and the user_data table"""
    get_cols()
    response = get_habits()
    raw_habits = ",".join(response[0])
    habits = raw_habits.split(",")
    missing_columns = set(habits) - set(cols)

    if missing_columns:
        try:
            with db.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                for i in missing_columns:
                    cursor.execute(f"ALTER TABLE habits ADD COLUMN {i} REAL")
            # print("syncing cols.... DONE")
        except db.Error as e:
            print(f"DatabaseError: {e}")


def track():
    """track today data if there's no data today"""
    get_cols()
    del cols[:2]
    columns = ",".join(cols)
    columns = "date," + columns
    data = []
    for col in cols:
        raw = float_input(f"enter value for {col}\n==>")
        data.append(raw)
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            data.insert(0, datetime.date.today())
            cursor.execute(
                f"INSERT INTO habits ({columns}) VALUES ({', '.join(['?' for _ in data])})",
                data,
            )
        print("habits tracked :)")
    except db.Error as e:
        print(f"Database error: {e}")


def get_habit(habit: str):
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {habit} from habits ORDER BY id DESC LIMIT 1")
            return cursor.fetchall()
    except db.Error as e:
        print(f"Database error {e}")
        return None


def track_habit(habit: str):
    cheers()
    check_cols()
    result = get_habit(habit)
    if result:
        print(f"you already tracked {habit}!")
        return
    push = float_input(f"enter value for {habit}:\n=> ")
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            today = datetime.date.today()
            cursor.execute(
                f"INSERT INTO habits (date,{habit}) VALUES(?,?)", (today, push)
            )
        print(f"{habit} tracked :)")
    except db.Error as e:
        print(f"Database error {e}")


def main():
    """main function"""
    cheers()
    check_cols()
    record = get_record()
    print(record)
    if record is None or record == []:
        track()
    # there are items in today track
    else:
        record = list(record[0])
        none_list = []
        for i, rec in enumerate(record):
            if rec is None:
                none_list.append(i)
        # none_list has none values
        if len(none_list) > 0:
            get_cols()
            none_cols = []
            # get cols names where there's none values
            for i in none_list:
                none_cols.append(cols[i])
            # update none records
            for col in none_cols:
                value = float_input(
                    f"{col} hasn't been tracked please enter today value\n==> "
                )
                try:
                    with db.connect(
                        database=DATABASE_PATH, detect_types=db.PARSE_DECLTYPES
                    ) as conn:
                        cursor = conn.cursor()
                        today = datetime.date.today()
                        cursor.execute(
                            f"UPDATE habits SET {col} = ? WHERE date = ?",
                            (value, today),
                        )
                        conn.commit()
                    print(f"{col} updated")
                except db.Error as e:
                    print(f"Database Error: {e}")
        else:
            print("everything's tracked")
