from track_habits import get_cols
from functions import int_input
import sqlite3, os, webbrowser
import matplotlib.pyplot as plt
import pandas as pd

cols = get_cols()
database_path = "user/user_data.db"
try:
    with sqlite3.connect(database=database_path) as conn:
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
file = "myfig.png"
webbrowser.open("file://" + os.path.abspath(file))

df = df.to_string(index=False)


def average():
    print("average")


def habit_graph():
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
    # selected 1st menu
    sel_menu = int_input("1. Habit Graph\n2. Average\n==> ")
    if sel_menu == 1:
        print("vol")
    else:
        print("p")


main()
