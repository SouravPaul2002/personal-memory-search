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

    return conn