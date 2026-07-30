import sqlite3
from datetime import datetime


class Database:

    def __init__(self, db_name="expense_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )

        # Expenses table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        self.conn.commit()

    # ==================================================
    # User Authentication Methods
    # ==================================================
    def register_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        return cursor.fetchone()

    def check_login(self, username, password):
        """Alias for login_user."""
        return self.login_user(username, password)

    # ==================================================
    # Expense CRUD Operations
    # ==================================================
    def add_expense(self, user_id, amount, category, description, date):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO expenses (user_id, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, description, date)
        )
        self.conn.commit()

    def get_recent_expenses(self, user_id, limit=50):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, amount, category, description, date
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        return cursor.fetchall()

    def get_expense_by_id(self, expense_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, amount, category, description, date FROM expenses WHERE id = ?",
            (expense_id,)
        )
        return cursor.fetchone()

    def get_expense(self, expense_id):
        """Alias for get_expense_by_id."""
        return self.get_expense_by_id(expense_id)

    def update_expense(self, expense_id, amount, category, description, date):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE expenses
            SET amount = ?, category = ?, description = ?, date = ?
            WHERE id = ?
            """,
            (amount, category, description, date, expense_id)
        )
        self.conn.commit()

    def delete_expense(self, expense_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

    # ==================================================
    # Summary Dashboard Metrics
    # ==================================================
    def get_total_expense(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()[0]
        return result if result else 0.0

    def get_month_expense(self, user_id):
        current_month = datetime.now().strftime("%m-%Y")
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT SUM(amount) FROM expenses
            WHERE user_id = ? AND date LIKE ?
            """,
            (user_id, f"%{current_month}%")
        )
        result = cursor.fetchone()[0]
        return result if result else 0.0

    def get_total_categories(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT COUNT(DISTINCT category) FROM expenses WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()[0]
        return result if result else 0

    # ==================================================
    # Live Search Operations
    # ==================================================
    def search_expenses(self, user_id, query):
        cursor = self.conn.cursor()
        search_pattern = f"%{query}%"
        cursor.execute(
            """
            SELECT id, amount, category, description, date
            FROM expenses
            WHERE user_id = ? AND (category LIKE ? OR description LIKE ?)
            ORDER BY date DESC, id DESC
            """,
            (user_id, search_pattern, search_pattern)
        )
        return cursor.fetchall()

    # ==================================================
    # Analytics & Export Methods
    # ==================================================
    def get_category_breakdown(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id = ?
            GROUP BY category
            HAVING SUM(amount) > 0
            """,
            (user_id,)
        )
        return cursor.fetchall()

    def get_monthly_spending(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT strftime('%Y-%m', date) as month, SUM(amount)
            FROM expenses
            WHERE user_id = ?
            GROUP BY month
            ORDER BY month ASC
            """,
            (user_id,)
        )
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows if row[0] is not None}

    def get_all_user_expenses(self, user_id):
        """Fetch all expenses for export (Date, Category, Description, Amount)."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT date, category, description, amount
            FROM expenses
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )
        return cursor.fetchall()