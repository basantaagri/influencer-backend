import sqlite3
from pathlib import Path

# -------------------------------------------------
# DATABASE LOCATION (UNCHANGED)
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"

# -------------------------------------------------
# GET DATABASE CONNECTION (SAFE)
# -------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Safe pragmas (do NOT break anything)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")

    return conn
