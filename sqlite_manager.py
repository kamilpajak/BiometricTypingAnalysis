import sqlite3


class SQLiteManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def close(self):
        """Close the database connection."""
        self.conn.close()
