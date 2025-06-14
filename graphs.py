"""
This module provides utility functions for database manipulation.
"""

import sqlite3
import os
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
from track_habits import get_cols
from functions import int_input
from config import DATABASE_PATH

cols = get_cols()
try:
    with sqlite3.connect(database=DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * from habits")
        results = cursor.fetchall()
        df = pd.DataFrame(results)
except sqlite3.Error as e:
    print(f"Database Error {e}")

df.columns = cols
x = df["water"].mean()
print(x)
df.plot(x="date", y=["weight"], kind="bar", title="Graph", figsize=(18, 10))
plt.axhline(y=x, color="gray", label="Average")
plt.savefig("myfig.png")
FILE = "myfig.png"
webbrowser.open("file://" + os.path.abspath(FILE))

df = df.to_string(index=False)


def average():
    """calculate the average of all the habits"""
    print("average")


def habit_graph():
    """simple menu to see habit graphs"""
    # selected menu in habit graph menu
    sel_menu = int_input("1. Week\n2. Month\n3. Year")
    if sel_menu == 1:
        print("week")
    elif sel_menu == 2:
        print("month")
    elif sel_menu == 3:
        print("year")
    else:
        print("please enter a valid option")


def main():
    """main function"""
    # selected 1st menu
    sel_menu = int_input("1. Habit Graph\n2. Average\n==> ")
    if sel_menu == 1:
        print("vol")
    else:
        print("p")


main()
