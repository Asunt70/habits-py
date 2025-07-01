"""date adapter for database"""

import sqlite3 as db
import datetime

# Adapter for date/datetime → SQLite
db.register_adapter(datetime.date, lambda d: d.isoformat())
db.register_adapter(datetime.datetime, lambda dt: dt.isoformat())

# Converter from SQLite → Python
db.register_converter("date", lambda b: datetime.date.fromisoformat(b.decode()))
db.register_converter("datetime", lambda b: datetime.datetime.fromisoformat(b.decode()))

# Enable converters when connecting
# conn = db.connect(database=DATABASE_PATH, detect_types=db.PARSE_DECLTYPES)
