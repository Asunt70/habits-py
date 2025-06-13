# WARNING THIS IS AN EXAMPLE
import sqlite3 as db
import csv

# Run your query, the result is stored as `data`
with db.connect("vehicles.db") as conn:
    cur = conn.cursor()
    sql = "SELECT make, style, color, plate FROM vehicle_vehicle"
    cur.execute(sql)
    data = cur.fetchall()

# Create the csv file
with open("vehicle.csv", "w", newline="") as f_handle:
    writer = csv.writer(f_handle)
    # Add the header/column names
    header = ["make", "style", "color", "plate"]
    writer.writerow(header)
    # Iterate over `data`  and  write to the csv file
    for row in data:
        writer.writerow(row)
