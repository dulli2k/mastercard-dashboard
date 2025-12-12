import os
import sqlite3

from src.backend.config import settings

def test_db_file_exists():
    assert os.path.exists(settings.DB_PATH)

def test_can_connect():
    conn = sqlite3.connect(settings.DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    conn.close()

def test_metrics_table_exists():
    conn = sqlite3.connect(settings.DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='metro_metrics'
    """)
    assert cur.fetchone() is not None
    conn.close()
