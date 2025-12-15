from __future__ import annotations

import sqlite3
from typing import Any, Dict, Generator, List, Optional

from .config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _normalize_params(params: Any | None) -> Any | None:
    """
    Normalize params to something sqlite3 understands:
    - dict -> dict (named params)
    - tuple/list -> tuple (positional)
    - None -> None
    """
    if params is None:
        return None

    if isinstance(params, dict):
        return params

    if isinstance(params, (list, tuple)):
        return tuple(params)

    return params


def query_db(query: str, params: Any | None = None) -> List[Dict[str, Any]]:
    """Run a SELECT query and return list[dict] rows."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        norm = _normalize_params(params)

        if norm is None:
            cur.execute(query)
        else:
            cur.execute(query, norm)

        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def fetch_all(query: str, params: Any | None = None) -> List[Dict[str, Any]]:
    """Alias for query_db (SELECT returning many)."""
    return query_db(query, params)


def fetch_one(
    query: str,
    params: Any | None = None,
) -> Optional[Dict[str, Any]]:
    """Run a SELECT query and return a single row dict or None."""
    rows = query_db(query, params)
    return rows[0] if rows else None


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    FastAPI dependency generator
    for a per-request DB connection.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
