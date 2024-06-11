import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.create_items_table()

    def create_items_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    gold_total INTEGER
                )
            """)

    def insert_item(self, item_id, name, description, gold_total):
        with self.connection:
            self.connection.execute("""
                INSERT INTO items (id, name, description, gold_total) 
                VALUES (?, ?, ?, ?)
            """, (item_id, name, description, gold_total))

    def fetch_all_items(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM items").fetchall()

    def close(self):
        self.connection.close()
