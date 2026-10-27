import json
import time
from backend.database.database import get_connection
from backend.database.schema import initialize_database as schema_init

def initialize_database():
    """Initializes database tables, indexes and performs one-time migrations."""
    schema_init()

def insert_file(
    *,
    file_uri,
    original_uri,
    file_name,
    file_type,
    mime_type,
    file_size,
    created_time,
    modified_time,
    last_access_time,
    content_hash,
    keywords=None,
    topics=None,
    summary=None,
):
    """Inserts a new file record into the files table or updates/un-deletes if already exists."""
    conn = get_connection()
    cursor = conn.cursor()
    now = time.time()
    cursor.execute(
        """
        INSERT INTO files (
            file_uri,
            original_uri,
            file_name,
            file_type,
            mime_type,
            file_size,
            created_time,
            modified_time,
            last_access_time,
            content_hash,
            last_indexed,
            last_scan_time,
            is_deleted,
            keywords,
            topics,
            summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
        ON CONFLICT(file_uri) DO UPDATE SET
            original_uri = COALESCE(excluded.original_uri, files.original_uri),
            file_name = excluded.file_name,
            file_type = excluded.file_type,
            mime_type = excluded.mime_type,
            file_size = excluded.file_size,
            created_time = excluded.created_time,
            modified_time = excluded.modified_time,
            last_access_time = excluded.last_access_time,
            content_hash = excluded.content_hash,
            last_indexed = excluded.last_indexed,
            last_scan_time = excluded.last_scan_time,
            is_deleted = 0,
            keywords = excluded.keywords,
            topics = excluded.topics,
            summary = excluded.summary
        """,
        (
            file_uri,
            original_uri,
            file_name,
            file_type,
            mime_type,
            file_size,
            created_time,
            modified_time,
            last_access_time or now,
            content_hash,
            now,
            now,
            json.dumps(keywords or []),
            json.dumps(topics or []),
            summary
        )
    )
    conn.commit()
    conn.close()

def update_file(
    *,
    file_uri,
    original_uri=None,
    file_name=None,
    file_type=None,
    mime_type=None,
    file_size=None,
    created_time=None,
    modified_time=None,
    last_access_time=None,
    content_hash=None,
    keywords=None,
    topics=None,
    summary=None,
):
    """Updates an existing file record in the files table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # We construct a dynamic query to only update fields that are provided (not None)
    updates = []
    params = []
    
    fields = {
        "original_uri": original_uri,
        "file_name": file_name,
        "file_type": file_type,
        "mime_type": mime_type,
        "file_size": file_size,
        "created_time": created_time,
        "modified_time": modified_time,
        "last_access_time": last_access_time,
        "content_hash": content_hash,
        "summary": summary
    }
    
    for field, val in fields.items():
        if val is not None:
            updates.append(f"{field} = ?")
            params.append(val)
            
    if keywords is not None:
        updates.append("keywords = ?")
        params.append(json.dumps(keywords))
        
    if topics is not None:
        updates.append("topics = ?")
        params.append(json.dumps(topics))
        
    # Always update last_indexed and last_scan_time when files are updated
    updates.append("last_indexed = ?")
    params.append(time.time())
    updates.append("last_scan_time = ?")
    params.append(time.time())
    
    # Make sure we un-delete it if it was deleted
    updates.append("is_deleted = 0")

    if not updates:
        conn.close()
        return

    query = f"UPDATE files SET {', '.join(updates)} WHERE file_uri = ?"
    params.append(file_uri)
    
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

def get_file(file_uri):
    """Retrieves a single file record by its file_uri (returns Row or None)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM files
        WHERE file_uri = ?
        """,
        (file_uri,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_files():
    """Retrieves all active (non-deleted) files (returns list of Row)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM files
        WHERE is_deleted = 0
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_deleted(file_uri):
    """Marks a file as deleted without removing it from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE files
        SET is_deleted = 1,
            last_scan_time = ?
        WHERE file_uri = ?
        """,
        (time.time(), file_uri)
    )
    conn.commit()
    conn.close()

def delete_file(file_uri):
    """Permanently deletes a file record from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM files
        WHERE file_uri = ?
        """,
        (file_uri,)
    )
    conn.commit()
    conn.close()

def update_last_scan_time(file_uri):
    """Updates the last_scan_time timestamp for a file."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE files
        SET last_scan_time = ?
        WHERE file_uri = ?
        """,
        (time.time(), file_uri)
    )
    conn.commit()
    conn.close()

# --- Helper functions for Upload Metadata ---

def save_upload_metadata(file_name, original_uri):
    """Saves or updates temporary upload metadata."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO uploads (file_name, original_uri)
        VALUES (?, ?)
        """,
        (file_name, original_uri)
    )
    conn.commit()
    conn.close()

def get_upload_metadata():
    """Returns a dictionary of all uploaded file mappings."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, original_uri FROM uploads")
    rows = cursor.fetchall()
    conn.close()
    return {row["file_name"]: {"original_uri": row["original_uri"]} for row in rows}

def clear_all_files():
    """Permanently deletes all file records from the database (used in full scan)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files")
    conn.commit()
    conn.close()