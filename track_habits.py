import sqlite3
from functions import int_input

database_path = "user/user_data.db"
cols = []  # declaring empty list for get_cols()


# get the cols from the database
def get_cols():
    try:
        with sqlite3.connect(database=database_path) as conn:
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


# get habits col from user_data table
def get_habits():
    try:
        with sqlite3.connect(database=database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT habits FROM user_data")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


# delete the today record
def delete_record():
    try:
        with sqlite3.connect(database=database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM habits WHERE date = CURRENT_DATE;")
            conn.commit()
        print(f"deleted record succesfully")
    except sqlite3.Error as e:
        print(f"Database Errro: {e}")


# get the today record
def get_record():
    try:
        with sqlite3.connect(database=database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from habits WHERE date = CURRENT_DATE;")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")


# track today data if there's no data today
def track():
    cols.clear()
    get_cols()
    cols.pop(0)
    columns = ",".join(cols)
    columns = "date," + columns
    data = []
    for col in cols:
        raw = int_input(f"insert data for {col}\n==>")
        data.append(raw)
    try:
        with sqlite3.connect(database=database_path) as conn:
            cursor = conn.cursor()
            data.insert(0, sqlite3.datetime.datetime.now().date())
            cursor.execute(
                f"INSERT INTO habits ({columns}) VALUES ({', '.join(['?' for _ in data])})",
                data,
            )
        print("Data INSERTED")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def check_cols():
    # past code
    # cols.clear()
    # get_cols()
    # new code
    get_cols()
    # print(cols)
    res = get_habits()
    unf_habits = ",".join(res[0])
    habits = unf_habits.split(",")
    diff = set(habits) - set(cols)

    if diff:
        try:
            with sqlite3.connect(database=database_path) as conn:
                cursor = conn.cursor()
                for i in diff:
                    cursor.execute(f"ALTER TABLE habits ADD COLUMN {i} INTEGER;")
            print(f"sync {diff} cols, DONE")
        except sqlite3.Error as e:
            print(f"DatabaseError: {e}")
    else:
        print("all cols are SYNCHRONYZED")


def main():
    check_cols()
    record = get_record()
    print(f"today record: {record}")
    # there's no track data today
    if record == []:
        track()
    # there are items in today track
    else:
        record = list(record[0])
        none_list = []
        for i in range(len(record)):
            if record[i] is None:
                none_list.append(i)
        if len(none_list) > 0:
            print(f"theres none values which are: {none_list}")
            cols.clear()
            get_cols()
            print(cols)
            for i in none_list:
                print(f"{cols[i]} has a none value in {i}")
        else:
            print("everything is tracked")


main()
