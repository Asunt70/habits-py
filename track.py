"""track habits"""

# ALLOW FLOAT
import sqlite3
import datetime
import utils.date_adapter as date_adapter  # noqa: F401  # <- Tells linters to chill
from utils.functions import float_input, get_habits, get_record
from config.config import DATABASE_PATH

cols = []  # declaring empty list for get_cols()


# get the cols from the database
def get_cols():
    """get cols from database returns a list"""
    cols.clear()
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            data = cursor.execute(
                """
                SELECT * FROM habits
            """
            )
            for column in data.description:
                cols.append(column[0])
            return cols
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


def check_cols():
    """check if there are differences between the habit table and the user_data table and updates it"""
    get_cols()
    response = get_habits()
    raw_habits = ",".join(response[0])
    habits = raw_habits.split(",")
    missing_columns = set(habits) - set(cols)

    if missing_columns:
        try:
            with sqlite3.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                for i in missing_columns:
                    cursor.execute(f"ALTER TABLE habits ADD COLUMN {i} REAL")
            print("syncing cols.... DONE")
        except sqlite3.Error as e:
            print(f"DatabaseError: {e}")
    # else:
    #     print("all cols are SYNCHRONYZED")


def track():
    """track today data if there's no data today"""
    get_cols()
    del cols[:2]
    columns = ",".join(cols)
    columns = "date," + columns
    data = []
    for col in cols:
        raw = float_input(f"insert data for {col}\n==>")
        data.append(raw)
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            data.insert(0, datetime.date.today())
            cursor.execute(
                f"INSERT INTO habits ({columns}) VALUES ({', '.join(['?' for _ in data])})",
                data,
            )
        print("habit(s) tracked successfully")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def main():
    """main function"""
    check_cols()
    record = get_record()
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
                print(f"{cols[i]} has a none value")
                none_cols.append(cols[i])
            # update none records
            for col in none_cols:
                value = float_input(f"{col} is none please enter value for today\n==> ")
                try:
                    with sqlite3.connect(
                        database=DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES
                    ) as conn:
                        cursor = conn.cursor()
                        today = datetime.date.today()
                        cursor.execute(
                            f"UPDATE habits SET {col} = ? WHERE date = ?",
                            (value, today),
                        )
                        conn.commit()
                    print(f"{col} UPDATED")
                except sqlite3.Error as e:
                    print(f"Database Error: {e}")
        # all cols are tracked
        else:
            print("everything is tracked")