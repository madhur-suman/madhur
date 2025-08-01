import sqlite3

conn = sqlite3.connect("inventory.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    item TEXT PRIMARY KEY,
    quantity INTEGER
)
""")
cur.executemany("INSERT OR REPLACE INTO inventory (item, quantity) VALUES (?, ?)", [
    ("maggi", 50),
    ("biscuits", 100),
    ("detergent", 30)
])
conn.commit()
conn.close()