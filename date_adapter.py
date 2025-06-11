import sqlite3, datetime

# Adapter for date/datetime → SQLite
sqlite3.register_adapter(datetime.date, lambda d: d.isoformat())
sqlite3.register_adapter(datetime.datetime, lambda dt: dt.isoformat())

# Converter from SQLite → Python
sqlite3.register_converter("date", lambda b: datetime.date.fromisoformat(b.decode()))
sqlite3.register_converter(
    "datetime", lambda b: datetime.datetime.fromisoformat(b.decode())
)

# Enable converters when connecting
conn = sqlite3.connect("user/user_data.db", detect_types=sqlite3.PARSE_DECLTYPES)
