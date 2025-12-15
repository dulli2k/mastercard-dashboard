import sqlite3

from src.backend.config import DB_PATH


def test_db_file_exists():
    assert DB_PATH.exists()


def test_can_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.close()
    assert True


def test_metrics_table_exists():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='metro_metrics';"
    )

    row = cur.fetchone()
    conn.close()
    assert row is not None
