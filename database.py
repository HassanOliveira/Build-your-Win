import sqlite3
import json
from riot_api import RiotAPI
import config

class Database:
    def __init__(self, db_name, riot_api):
        self.connection = sqlite3.connect(db_name)
        self.riot_api = riot_api
        self.create_items_table()
        self.create_rune_tables()

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

    def create_rune_tables(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS rune_paths (
                    id INTEGER PRIMARY KEY,
                    key TEXT,
                    icon TEXT,
                    name TEXT
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS rune_slots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rune_path_id INTEGER,
                    slot_index INTEGER,
                    is_primary BOOLEAN,
                    FOREIGN KEY (rune_path_id) REFERENCES rune_paths (id)
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS runes (
                    id INTEGER PRIMARY KEY,
                    key TEXT,
                    icon TEXT,
                    name TEXT,
                    shortDesc TEXT,
                    longDesc TEXT,
                    rune_slot_id INTEGER,
                    FOREIGN KEY (rune_slot_id) REFERENCES rune_slots (id)
                )
            """)

    def insert_items(self):
        items_data = self.riot_api.get_all_items()
        for item_id, item in items_data['data'].items():
            with self.connection:
                self.connection.execute("""
                    INSERT INTO items (
                        id, name, description, plaintext, gold_base, gold_total, gold_sell, purchasable, into_items, tags, maps, stats, image_full, image_sprite, image_group, image_x, image_y, image_w, image_h
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(item_id),
                    item['name'],
                    item.get('description', ''),
                    item.get('plaintext', ''),
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

    def insert_runes(self):
        data = self.riot_api.get_all_runes()
        
        with self.connection:
            for path in data:
                self.connection.execute('''
                    INSERT INTO rune_paths (id, key, icon, name)
                    VALUES (?, ?, ?, ?)
                ''', (path['id'], path['key'], path['icon'], path['name']))
                
                for slot_index, slot in enumerate(path['slots']):
                    is_primary = (slot_index == 0)
                    self.connection.execute('''
                        INSERT INTO rune_slots (rune_path_id, slot_index, is_primary)
                        VALUES (?, ?, ?)
                    ''', (path['id'], slot_index, is_primary))
                    slot_id = self.connection.execute('SELECT last_insert_rowid()').fetchone()[0]
                    
                    for rune in slot['runes']:
                        self.connection.execute('''
                            INSERT INTO runes (id, key, icon, name, shortDesc, longDesc, rune_slot_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (rune['id'], rune['key'], rune['icon'], rune['name'], rune['shortDesc'], rune['longDesc'], slot_id))

    def fetch_all_items(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM items").fetchall()

    def fetch_all_runes(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM runes").fetchall()

    def close(self):
        self.connection.close()

# Exemplo de uso
riot_api = RiotAPI(config.API_KEY, config.REGION)
db = Database(config.DATABASE, riot_api)
db.insert_items()
db.insert_runes()
items = db.fetch_all_items()
runes = db.fetch_all_runes()
db.close()