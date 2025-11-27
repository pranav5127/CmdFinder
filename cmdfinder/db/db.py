import sqlite3
from contextlib import contextmanager
from cmdfinder.config.config import DB_PATH
from cmdfinder.utils.logger import logger

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    create_cmd_table = """
        CREATE TABLE IF NOT EXISTS commands(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            ts INTEGER
        );

        CREATE INDEX IF NOT EXISTS idx_history_command 
            ON commands(command);
    """
    with get_conn() as connection:
        cursor = connection.cursor()
        cursor.executescript(create_cmd_table)
        logger.info("db created successfully at ~/.cmdfinder.db")
