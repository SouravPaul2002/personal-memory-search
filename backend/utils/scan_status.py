# backend/utils/scan_status.py

from backend.database.database import get_connection


def load_scan_status() -> dict:
    """Returns the current scan status row as a dict, or {} if none exists."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT last_scan_time, last_scan_type FROM scan_status WHERE id = 1"
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return {}
    return {
        "last_scan_time": row["last_scan_time"],
        "last_scan_type": row["last_scan_type"],
    }


def save_scan_status(last_scan_time: str, last_scan_type: str) -> None:
    """Upserts the scan status into SQLite (always row id=1)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO scan_status (id, last_scan_time, last_scan_type)
        VALUES (1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            last_scan_time = excluded.last_scan_time,
            last_scan_type = excluded.last_scan_type
        """,
        (last_scan_time, last_scan_type),
    )
    conn.commit()
    conn.close()