"""Export habits to a CSV file."""

import sqlite3 as db
import csv
import os
from habitpy.config.config import DATABASE_PATH, EXPORT_PATH


def read_data():
    """reads habits data from database"""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM habits")
            cols = [desc[0] for desc in cur.description]
            data = cur.fetchall()
            return cols, data
    except db.Error as e:
        print(f"Database error: {e}")
        return None


def write_csv(cols, data):
    """writes habits data into a csv file"""
    with open(EXPORT_PATH, "w", newline="", encoding="utf-8") as f_handle:
        writer = csv.writer(f_handle)
        header = cols
        writer.writerow(header)
        for row in data:
            writer.writerow(row)


def main(show: bool):
    """Export habits to a CSV file."""
    cols, data = read_data()
    if data is None or data == []:
        if show is True:
            print("no data to export! please run 'habitpy track'")
        return
    if os.path.exists(EXPORT_PATH):
        os.remove(EXPORT_PATH)
    write_csv(cols, data)
    print(f"your data has been exported into {EXPORT_PATH}, save the file!")
