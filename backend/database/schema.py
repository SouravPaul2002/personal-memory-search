from .database import get_connection
import os
import json
import time
from datetime import datetime


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS files (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,

    -- File identity
    file_uri          TEXT    NOT NULL UNIQUE,
    original_uri      TEXT,

    -- Basic file information
    file_name         TEXT    NOT NULL,
    file_type         TEXT    NOT NULL
                              CHECK (file_type IN ('pdf', 'image', 'txt', 'docx', 'pptx')),
    mime_type         TEXT,
    file_size         INTEGER,

    -- File timestamps
    created_time      REAL,
    modified_time     REAL,
    last_access_time  REAL,

    -- Indexing
    content_hash      TEXT    NOT NULL,
    last_indexed      REAL,
    last_scan_time    REAL,

    -- Status
    is_deleted        INTEGER NOT NULL DEFAULT 0,

    -- AI Metadata
    keywords          TEXT,
    topics            TEXT,
    summary           TEXT
);
"""

CREATE_UPLOADS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS uploads (
    file_name    TEXT    PRIMARY KEY,
    original_uri TEXT    NOT NULL
);
"""

INDEXES = [

"""
CREATE INDEX IF NOT EXISTS idx_files_file_name
ON files(file_name);
""",

"""
CREATE INDEX IF NOT EXISTS idx_files_file_type
ON files(file_type);
""",

"""
CREATE INDEX IF NOT EXISTS idx_files_content_hash
ON files(content_hash);
""",

"""
CREATE INDEX IF NOT EXISTS idx_files_modified_time
ON files(modified_time);
""",

"""
CREATE INDEX IF NOT EXISTS idx_files_last_access
ON files(last_access_time);
""",

"""
CREATE INDEX IF NOT EXISTS idx_files_deleted
ON files(is_deleted);
"""
]


CREATE_SCAN_STATUS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS scan_status (
    id              INTEGER PRIMARY KEY DEFAULT 1,
    last_scan_time  TEXT,
    last_scan_type  TEXT
);
"""

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(CREATE_TABLE_SQL)
    cursor.execute(CREATE_UPLOADS_TABLE_SQL)
    cursor.execute(CREATE_SCAN_STATUS_TABLE_SQL)

    for index in INDEXES:
        cursor.execute(index)

    conn.commit()

    # --- Migration: data/upload_metadata.json to uploads table ---
    cursor.execute("SELECT COUNT(*) FROM uploads")
    uploads_count = cursor.fetchone()[0]
    upload_metadata_file = "data/upload_metadata.json"

    if uploads_count == 0 and os.path.exists(upload_metadata_file):
        try:
            with open(upload_metadata_file, "r", encoding="utf-8") as f:
                upload_metadata = json.load(f)
            if upload_metadata:
                for file_name, val in upload_metadata.items():
                    original_uri = val.get("original_uri")
                    if original_uri:
                        cursor.execute(
                            "INSERT OR REPLACE INTO uploads (file_name, original_uri) VALUES (?, ?)",
                            (file_name, original_uri)
                        )
                conn.commit()
                print(f"Migrated {len(upload_metadata)} entries from upload_metadata.json to database.")
                try:
                    os.rename(upload_metadata_file, upload_metadata_file + ".bak")
                except Exception as rename_err:
                    print(f"Error renaming upload_metadata.json: {rename_err}")
        except Exception as e:
            print(f"Error migrating upload_metadata.json: {e}")

    # --- Migration: backend/indexing/file_registry.json to files table ---
    cursor.execute("SELECT COUNT(*) FROM files")
    files_count = cursor.fetchone()[0]
    registry_file = "backend/indexing/file_registry.json"

    if files_count == 0 and os.path.exists(registry_file):
        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                registry = json.load(f)
            if registry:
                for file_uri, data in registry.items():
                    last_indexed_val = data.get("last_indexed")
                    if last_indexed_val:
                        if isinstance(last_indexed_val, str):
                            try:
                                last_indexed_ts = datetime.fromisoformat(last_indexed_val).timestamp()
                            except Exception:
                                last_indexed_ts = time.time()
                        else:
                            last_indexed_ts = float(last_indexed_val)
                    else:
                        last_indexed_ts = time.time()

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO files (
                            file_uri, original_uri, file_name, file_type, mime_type, file_size,
                            created_time, modified_time, last_access_time, content_hash,
                            last_indexed, last_scan_time, is_deleted, keywords, topics, summary
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
                        """,
                        (
                            file_uri,
                            data.get("original_uri"),
                            data["file_name"],
                            data["file_type"],
                            data.get("mime_type"),
                            data.get("file_size"),
                            data.get("created_time"),
                            data.get("modified_time"),
                            data.get("last_access_time") or time.time(),
                            data["content_hash"],
                            last_indexed_ts,
                            time.time(),
                            json.dumps(data.get("keywords") or []),
                            json.dumps(data.get("topics") or []),
                            data.get("summary")
                        )
                    )
                conn.commit()
                print(f"Migrated {len(registry)} entries from file_registry.json to database.")
                try:
                    os.rename(registry_file, registry_file + ".bak")
                except Exception as rename_err:
                    print(f"Error renaming file_registry.json: {rename_err}")
        except Exception as e:
            print(f"Error migrating file_registry.json: {e}")

    conn.close()
    print("SQLite database initialized.")