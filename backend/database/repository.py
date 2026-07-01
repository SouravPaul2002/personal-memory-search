import json
import time

from .database import get_connection

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

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO files(
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
            keywords,
            topics,
            summary
        )

        VALUES(
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?
        )
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
            last_access_time,
            content_hash,
            time.time(),
            time.time(),
            json.dumps(keywords or []),
            json.dumps(topics or []),
            summary

        )

    )

    conn.commit()
    conn.close()


def get_file(file_uri):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT *
        FROM files
        WHERE file_uri=?
        """,

        (file_uri,)

    )

    row = cursor.fetchone()

    conn.close()

    return row


def get_all_files():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT *
        FROM files
        WHERE is_deleted=0
        """

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def mark_deleted(file_uri):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        UPDATE files
        SET
            is_deleted=1,
            last_scan_time=?
        WHERE file_uri=?
        """,

        (

            time.time(),
            file_uri

        )

    )

    conn.commit()

    conn.close()

def update_last_scan(file_uri):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        UPDATE files
        SET last_scan_time=?
        WHERE file_uri=?
        """,

        (time.time(), file_uri)

    )

    conn.commit()

    conn.close()