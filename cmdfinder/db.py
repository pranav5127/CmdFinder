import sqlite3
from pathlib import Path

DB_PATH = Path("~/.cmdfinder.db").expanduser()

def init_db():

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        print("Db connected successfully.")

        create_cmd_table = """
        CREATE TABLE IF NOT EXISTS commands(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            ts INTEGER
        );
        
        CREATE INDEX IF NOT EXISTS idx_history_command 
            ON history(command);
        
    """
        cursor.executescript(create_cmd_table)
        connection.commit()

        print("Table 'cmdfinder' created successfully!")

if __name__ == "__main__":
    init_db()

