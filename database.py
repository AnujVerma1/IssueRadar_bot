"""
database.py — SQLite storage for notified issue tracking.
Prevents duplicate Telegram notifications.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "issueradar.db")


def _get_connection():
    """Return a connection to the SQLite database, creating tables if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notified_issues (
            issue_id   INTEGER PRIMARY KEY,
            repo       TEXT    NOT NULL,
            title      TEXT    NOT NULL,
            url        TEXT    NOT NULL,
            notified_at TEXT   NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    return conn


def is_notified(issue_id: int) -> bool:
    """Check whether an issue has already been notified."""
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT 1 FROM notified_issues WHERE issue_id = ?", (issue_id,)
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def mark_notified(issue_id: int, repo: str, title: str, url: str) -> None:
    """Record an issue as notified so it won't be sent again."""
    conn = _get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO notified_issues (issue_id, repo, title, url) VALUES (?, ?, ?, ?)",
            (issue_id, repo, title, url),
        )
        conn.commit()
    finally:
        conn.close()
