import sqlite3
from habitpy.config.config import DATABASE_PATH
import datetime


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
