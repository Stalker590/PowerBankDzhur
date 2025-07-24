import os
import sqlite3
import time
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'power_banks.db')

def retry_db_operation(func, max_retries=3, delay=0.1):
    """Retry database operation in case of locks"""
    for attempt in range(max_retries):
        try:
            return func()
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
                continue
            raise
        except Exception:
            raise

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row  # Дозволяє отримувати dict-подібні результати
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        conn.execute('PRAGMA journal_mode=WAL;')
        conn.execute('PRAGMA synchronous=NORMAL;')
        conn.execute('PRAGMA cache_size=1000;')
        conn.execute('PRAGMA temp_store=memory;')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS power_banks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                capacity INTEGER NOT NULL,
                description TEXT,
                number INTEGER UNIQUE NOT NULL
            )
        ''')

def add_power_bank(name, price, capacity, description, number):
    def _add_data():
        try:
            with get_db_connection() as conn:
                with conn:
                    conn.execute(
                        "INSERT INTO power_banks (name, price, capacity, description, number) VALUES (?, ?, ?, ?, ?)",
                        (name, price, capacity, description, number)
                    )
            print(f"PowerBank '{name}' added successfully.")
            return True
        except sqlite3.IntegrityError:
            print(f"PowerBank with number {number} already exists.")
            return False
    return retry_db_operation(_add_data)

def get_all_power_banks():
    def _get_data():
        with get_db_connection() as conn:
            cursor = conn.execute("SELECT name, price, capacity, description, number FROM power_banks")
            return [dict(row) for row in cursor.fetchall()]
    return retry_db_operation(_get_data)

def delete_power_bank(number):
    def _delete_data():
        with get_db_connection() as conn:
            with conn:
                cursor = conn.execute("DELETE FROM power_banks WHERE number = ?", (number,))
                return cursor.rowcount > 0
    return retry_db_operation(_delete_data)

if __name__ == '__main__':
    init_db()
    # Приклади
    add_power_bank("PowerBank 1", 1000.0, 10000, "Опис PowerBank 1", 1)
    add_power_bank("PowerBank 2", 1500.0, 20000, "Опис PowerBank 2", 2)
    add_power_bank("PowerBank 3", 2000.0, 30000, "Опис PowerBank 3", 3)

    print("\nAll PowerBanks in DB:")
    for pb in get_all_power_banks():
        print(pb)
