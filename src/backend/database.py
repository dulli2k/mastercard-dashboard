#Provide small, reusable helpers so the rest of your backend doesn’t have to think about SQLite details.
import sqlite3
from typing import Any, Iterator

from .config import DB_PATH

#Get a DB connection
def get_connection() -> sqlite3.Connection:
    """
    Create a new SQLite connection to the metro_metrics database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn


def get_db() -> Iterator[sqlite3.Connection]:
    """
    FastAPI-style dependency that yields a DB connection.

    tests/test_app.py imports this symbol and overrides it with an
    in-memory test database, so it just needs to exist and work.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

#normalize parameters
def _normalize_params(params: Any | None = None) -> Any | None:
    """
    Normalize parameters for sqlite3.execute.

    - dict  -> dict (named params)
    - list/tuple -> as-is (positional params)
    - single scalar -> (scalar,) tuple
    """
    if params is None:
        return None
    if isinstance(params, dict):
        return params
    if isinstance(params, (list, tuple)):
        return params
    return (params,)

#core query function
def query_db(query: str, params: Any | None = None) -> list[dict[str, Any]]:
    """
    Run a SELECT query and return a list of dict rows.
    """
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
    """
    Convenience wrapper to get all rows.
    """
    return query_db(query, params)


def fetch_one(query: str, params: Any | None = None) -> dict[str, Any] | None:
    """
    Convenience wrapper to get a single row (or None).
    """
    rows = query_db(query, params)
    return rows[0] if rows else None
