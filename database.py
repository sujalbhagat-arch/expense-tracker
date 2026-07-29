import sqlite3


class Database:

    def __init__(self):
        self.connection = sqlite3.connect("database/expense.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    # ------------------------
    # Create Users Table
    # ------------------------
    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.connection.commit()

    # ------------------------
    # Register New User
    # ------------------------
    def add_user(self, name, username, password):
        self.cursor.execute("""
        INSERT INTO users(name, username, password)
        VALUES (?, ?, ?)
        """, (name, username, password))

        self.connection.commit()

    # ------------------------
    # Login User
    # ------------------------
    def check_login(self, username, password):
        self.cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """, (username, password))

        return self.cursor.fetchone()