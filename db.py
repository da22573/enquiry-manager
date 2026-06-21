"""SQLite storage for enquiries."""

from __future__ import annotations

import sqlite3
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
DATABASE_PATH = APP_ROOT / "data" / "enquiries.db"


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS enquiries (
                id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL DEFAULT '',
                service TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                submitted_at TEXT NOT NULL
            )
            """
        )


def row_to_enquiry(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "fullName": row["full_name"],
        "email": row["email"],
        "phone": row["phone"],
        "service": row["service"],
        "description": row["description"],
        "status": row["status"],
        "submittedAt": row["submitted_at"],
    }


def insert_enquiry(enquiry: dict) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO enquiries (
                id, full_name, email, phone, service, description, status, submitted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                enquiry["id"],
                enquiry["fullName"],
                enquiry["email"],
                enquiry["phone"],
                enquiry["service"],
                enquiry["description"],
                enquiry["status"],
                enquiry["submittedAt"],
            ),
        )


def fetch_enquiries(
    query: str = "",
    service: str = "",
    status: str = "",
) -> list[dict]:
    sql = """
        SELECT id, full_name, email, phone, service, description, status, submitted_at
        FROM enquiries
        WHERE 1 = 1
    """
    params: list[str] = []

    if service:
        sql += " AND service = ?"
        params.append(service)

    if status:
        sql += " AND status = ?"
        params.append(status)

    if query:
        sql += """
            AND lower(full_name || ' ' || email || ' ' || service || ' ' || status) LIKE ?
        """
        params.append(f"%{query.lower()}%")

    sql += " ORDER BY submitted_at DESC"

    with get_connection() as connection:
        rows = connection.execute(sql, params).fetchall()

    return [row_to_enquiry(row) for row in rows]


def update_enquiry_status(enquiry_id: str, status: str) -> dict | None:
    with get_connection() as connection:
        connection.execute(
            "UPDATE enquiries SET status = ? WHERE id = ?",
            (status, enquiry_id),
        )
        row = connection.execute(
            """
            SELECT id, full_name, email, phone, service, description, status, submitted_at
            FROM enquiries
            WHERE id = ?
            """,
            (enquiry_id,),
        ).fetchone()

    if row is None:
        return None

    return row_to_enquiry(row)
