import sqlite3


class Database:

    def __init__(self):
        self.connection = sqlite3.connect("database/expense.db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    # ------------------------
    # Create Tables
    # ------------------------
    def create_tables(self):

        # Users Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        # Expenses Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        self.connection.commit()

    # ------------------------
    # Add New User
    # ------------------------
    def add_user(self, name, username, password):

        self.cursor.execute("""
        INSERT INTO users(name, username, password)
        VALUES (?, ?, ?)
        """, (name, username, password))

        self.connection.commit()

    # ------------------------
    # Check Login
    # ------------------------
    def check_login(self, username, password):

        self.cursor.execute("""
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """, (username, password))

        return self.cursor.fetchone()

    # ------------------------
    # Add Expense
    # ------------------------
    def add_expense(self, user_id, amount, category, description, expense_date):

        self.cursor.execute("""
        INSERT INTO expenses(
            user_id,
            amount,
            category,
            description,
            expense_date
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            amount,
            category,
            description,
            expense_date
        ))

        self.connection.commit()

    # ------------------------
    # Get All Expenses
    # ------------------------
    def get_expenses(self, user_id):

        self.cursor.execute("""
        SELECT *
        FROM expenses
        WHERE user_id=?
        ORDER BY expense_date DESC
        """, (user_id,))

        return self.cursor.fetchall()

    # ------------------------
    # Get Total Expense
    # ------------------------
    def get_total_expense(self, user_id):

        self.cursor.execute("""
        SELECT IFNULL(SUM(amount), 0)
        FROM expenses
        WHERE user_id=?
        """, (user_id,))

        return self.cursor.fetchone()[0]

    # ------------------------
    # Get Total Categories
    # ------------------------
    def get_total_categories(self, user_id):

        self.cursor.execute("""
        SELECT COUNT(DISTINCT category)
        FROM expenses
        WHERE user_id=?
        """, (user_id,))

        return self.cursor.fetchone()[0]

    # ------------------------
    # Get Recent Expenses
    # ------------------------
    def get_recent_expenses(self, user_id):

        self.cursor.execute("""
        SELECT amount, category, expense_date
        FROM expenses
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 5
        """, (user_id,))

        return self.cursor.fetchall()