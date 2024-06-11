import sqlite3
import json

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
                    plaintext TEXT,
                    gold_base INTEGER,
                    gold_total INTEGER,
                    gold_sell INTEGER,
                    purchasable BOOLEAN,
                    into_items TEXT,
                    tags TEXT,
                    maps TEXT,
                    stats TEXT,
                    image_full TEXT,
                    image_sprite TEXT,
                    image_group TEXT,
                    image_x INTEGER,
                    image_y INTEGER,
                    image_w INTEGER,
                    image_h INTEGER
                )
            """)

    def insert_item(self, item):
        with self.connection:
            self.connection.execute("""
                INSERT INTO items (
                    id, name, description, plaintext, gold_base, gold_total, gold_sell, purchasable, into_items, tags, maps, stats, image_full, image_sprite, image_group, image_x, image_y, image_w, image_h
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item['id'],
                item['name'],
                item['description'],
                item['plaintext'],
                item['gold']['base'],
                item['gold']['total'],
                item['gold']['sell'],
                item['gold']['purchasable'],
                json.dumps(item.get('into', [])),
                json.dumps(item.get('tags', [])),
                json.dumps(item.get('maps', {})),
                json.dumps(item.get('stats', {})),
                item['image']['full'],
                item['image']['sprite'],
                item['image']['group'],
                item['image']['x'],
                item['image']['y'],
                item['image']['w'],
                item['image']['h']
            ))

    def fetch_all_items(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM items").fetchall()

    def close(self):
        self.connection.close()
