import os
import sqlite3

database_path = 'user/habits.db'
if not os.path.exists(database_path):
    with sqlite3.connect(database=database_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE habits (
                date TEXT,
                habit TEXT,
                input INTEGER
            )
            ''')

