"""track habits"""

# ALLOW FLOAT
import sqlite3
import datetime
import date_adapter  # noqa: F401  # <- Tells linters to chill
from functions import int_input, get_habits
from config import DATABASE_PATH

cols = []  # declaring empty list for get_cols()


# get the cols from the database
def get_cols():
    """get cols from database returns a list"""
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


# delete the today record
def delete_record():
    """delete the last record TESTING ONLY"""
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            today = datetime.date.today()
            cursor.execute("DELETE FROM habits WHERE date = ?;", (today,))
            conn.commit()
        print("deleted record succesfully")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")


# get the today record
def get_record():
    """gets today record returns a tuple"""
    try:
        with sqlite3.connect(
            database=DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES
        ) as conn:
            cursor = conn.cursor()
            today = datetime.date.today()
            cursor.execute("SELECT * from habits WHERE date = ?", (today,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None


# lab function
def get_last_record():
    """gets last record returns a tuple"""
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habits ORDER BY ID DESC LIMIT 1")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database Erro: {e}")
        return None


def check_cols():
    "check if there are differences between the habit table and the user_data table and updates it"
    get_cols()
    res = get_habits()
    unf_habits = ",".join(res[0])
    habits = unf_habits.split(",")
    diff = set(habits) - set(cols)

    if diff:
        try:
            with sqlite3.connect(database=DATABASE_PATH) as conn:
                cursor = conn.cursor()
                for i in diff:
                    cursor.execute(f"ALTER TABLE habits ADD COLUMN {i} INTEGER;")
            print(f"sync {diff} cols, DONE")
        except sqlite3.Error as e:
            print(f"DatabaseError: {e}")
    # else:
    #     print("all cols are SYNCHRONYZED")


def track():
    """track today data if there's no data today"""
    cols.clear()
    get_cols()
    del cols[:2]
    columns = ",".join(cols)
    columns = "date," + columns
    data = []
    for col in cols:
        raw = int_input(f"insert data for {col}\n==>")
        data.append(raw)
    try:
        with sqlite3.connect(database=DATABASE_PATH) as conn:
            cursor = conn.cursor()
            data.insert(0, datetime.date.today())
            cursor.execute(
                f"INSERT INTO habits ({columns}) VALUES ({', '.join(['?' for _ in data])})",
                data,
            )
        print("done")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def main():
    """main function"""
    check_cols()
    record = get_record()
    # print(f"got record is: {record}")
    # there's no track data today
    if record == []:
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
            cols.clear()
            get_cols()
            none_cols = []
            # get cols names where there's none values
            for i in none_list:
                print(f"{cols[i]} has a none value")
                none_cols.append(cols[i])
            # update none records
            for col in none_cols:
                value = int_input(f"{col} is none please enter value for today\n==> ")
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
