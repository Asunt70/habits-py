"""Export habits to a CSV file."""

import sqlite3 as db
import csv
from habitpy.config.config import DATABASE_PATH


# Run your query, the result is stored as `data`
def main():
    """Export habits to a CSV file."""
    try:
        with db.connect(database=DATABASE_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM habits")
            cols = [desc[0] for desc in cur.description]
            data = cur.fetchall()
    except db.Error as e:
        print(f"Database error: {e}")
        return None

    # Create the csv file
    with open("exported.csv", "w", newline="", encoding="utf-8") as f_handle:
        writer = csv.writer(f_handle)
        # Add the header/column names
        header = cols
        writer.writerow(header)
        # Iterate over `data`  and  write to the csv file
        for row in data:
            writer.writerow(row)
