import sqlite3

def add_image_column(db_path="database.db"):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """)
    connection.commit()
    connection.close()
    print("Added users table")

if __name__ == "__main__":
    add_image_column()