import sqlite3
from pathlib import Path

# Absolute path anchored to this file's location — never depends on CWD
_HERE = Path(__file__).resolve().parent          # backend/database/
_PROJECT_ROOT = _HERE.parent.parent              # project root

DB_PATH = _PROJECT_ROOT / "backend" / "database" / "files.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")

    # WAL mode: readers and writers don't block each other
    conn.execute("PRAGMA journal_mode = WAL;")

    # Retry for up to 5s before raising "database is locked"
    conn.execute("PRAGMA busy_timeout = 5000;")

    return conn