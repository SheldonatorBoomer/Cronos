import sqlite3
import os

# Check where the database is being created
print(f"Starting the Database Setup!")

try:
    conn = sqlite3.connect("Cronos.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sites (
            urlHash TEXT PRIMARY KEY,
            url TEXT,
            title TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Crawler (
            urlHash TEXT PRIMARY KEY,
            url TEXT,
            lastChecked TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Terms (
            termId INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT,
            urlHash TEXT,
            position INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CrawlerToDo (
            urlId INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE
        )
    """)
    conn.commit()

    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables in the database:", [table[0] for table in cursor.fetchall()])

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    if conn:
        conn.close()
