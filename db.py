import uuid
import logging
import json
import sqlite3
from datetime import datetime, timedelta
from config import Config
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Resolve database file path from Config.DATABASE_URL
parsed = urlparse(Config.DATABASE_URL)
DATABASE_FILE = parsed.path.lstrip('/') if parsed.scheme == 'sqlite' else 'sales.db'

def create_database():
    """Create the SQLite database with schema and sample data"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shops (
                id TEXT PRIMARY KEY,
                name TEXT,
                owner_phone TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                shop_id TEXT REFERENCES shops(id),
                name TEXT,
                cost_price REAL,
                selling_price REAL,
                expiry_date TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id TEXT PRIMARY KEY,
                item_id TEXT REFERENCES items(id),
                quantity_sold INTEGER,
                profit REAL,
                sale_date TEXT DEFAULT CURRENT_DATE
            )
        ''')

        # Clear existing data
        cursor.execute('DELETE FROM sales')
        cursor.execute('DELETE FROM items')
        cursor.execute('DELETE FROM shops')

        # Add sample data
        populate_sample_data_sqlite(cursor)

        conn.commit()
        conn.close()

        logger.info("SQLite database created and sample data populated successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        return False

def populate_sample_data_sqlite(cursor):
    """Populate the SQLite database with sample data"""
    # (same as your current code — no change)
    # ...

def get_shop_id_by_phone(phone_number):
    """Get shop ID by phone number"""
    # (same as your current code — no change)

def execute_query(query, params=None, phone_number=None):
    """Execute a SQL query and return results"""
    # (same as your current code — no change)

def get_expiring_items(days=3):
    """Get items that will expire within the specified number of days"""
    # (same as your current code — no change)

def get_database_schema_info():
    """Get the database schema information for AI prompts"""
    # (same as your current code — no change)

def create_database_schema():
    """Legacy function - redirects to create_database"""
    return create_database()

# --- NEW HELPERS for Streamlit ---
def fetch_items_data():
    """Return all items (for Streamlit or analytics)"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def fetch_sales_data():
    """Return all sales (for Streamlit or analytics)"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(columns, row)) for row in rows]
