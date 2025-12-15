import sqlite3
from typing import Any

from .config import settings


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _normalize_params(params: Any | None):
    # Allow None, tuple/list, or dict params
    if params is None:
        return None
    if isinstance(params, (tuple, list, dict)):
        return params
    # Single value -> tuple
    return (params,)


def query_db(query: str, params: Any | None = None) -> list[dict[str, Any]]:
    """Run a SELECT query and return a list of dict rows."""
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


def fetch_all(query: str, params: Any | None = None) -> list[dict[str, Any]]:
    return query_db(query, params)


def fetch_one(query: str, params: Any | None = None) -> dict[str, Any] | None:
    rows = query_db(query, params)
    return rows[0] if rows else None

def get_db():
    """
    FastAPI-style dependency / test helper.
    Yields a sqlite connection and guarantees it closes.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
