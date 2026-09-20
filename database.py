import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).with_name("aft_sbtvc.db")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                meeting_date TEXT NOT NULL,
                meeting_time TEXT NOT NULL,
                location TEXT NOT NULL,
                details TEXT,
                created_by INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS attendance_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                is_open INTEGER NOT NULL DEFAULT 1,
                created_by INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                closed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS attendance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                display_name TEXT NOT NULL,
                checked_in_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id, user_id),
                FOREIGN KEY(session_id) REFERENCES attendance_sessions(id)
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                details TEXT,
                assignee_id INTEGER,
                assignee_name TEXT,
                due_date TEXT,
                status TEXT NOT NULL DEFAULT 'กำลังดำเนินการ',
                created_by INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            );
            """
        )


def execute(query: str, params: tuple[Any, ...] = ()) -> int:
    with connect() as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return int(cursor.lastrowid)


def fetchone(query: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute(query, params).fetchone()


def fetchall(query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(query, params).fetchall()
