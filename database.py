import sqlite3
from datetime import datetime, timedelta


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
                password TEXT NOT NULL,
                budget REAL DEFAULT 0.0
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
                payment_method TEXT DEFAULT 'UPI',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )

        # Ensure payment_method column exists in older DB files
        try:
            cursor.execute("ALTER TABLE expenses ADD COLUMN payment_method TEXT DEFAULT 'UPI'")
        except sqlite3.OperationalError:
            pass

        # Category Budgets Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS category_budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                budget_limit REAL NOT NULL,
                UNIQUE(user_id, category),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )

        self.conn.commit()

    # ==================================================
    # User Authentication & Overall Budget
    # ==================================================
    def register_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, budget) VALUES (?, ?, 0.0)",
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

    def set_user_budget(self, user_id, budget_amount):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET budget = ? WHERE id = ?", (budget_amount, user_id))
        self.conn.commit()

    def get_user_budget(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT budget FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0.0

    # ==================================================
    # Category Budget Operations (Option 3)
    # ==================================================
    def set_category_budget(self, user_id, category, limit_amount):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO category_budgets (user_id, category, budget_limit)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, category) DO UPDATE SET budget_limit = excluded.budget_limit
            """,
            (user_id, category, limit_amount)
        )
        self.conn.commit()

    def get_category_budgets(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT category, budget_limit FROM category_budgets WHERE user_id = ?",
            (user_id,)
        )
        return dict(cursor.fetchall())

    def get_category_month_spending(self, user_id, category):
        current_month = datetime.now().strftime("%m-%Y")
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT SUM(amount) FROM expenses
            WHERE user_id = ? AND category = ? AND date LIKE ?
            """,
            (user_id, category, f"%{current_month}%")
        )
        result = cursor.fetchone()[0]
        return result if result else 0.0

    # ==================================================
    # Expense CRUD Operations (Option 6: Payment Methods)
    # ==================================================
    def add_expense(self, user_id, amount, category, description, date, payment_method="UPI"):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO expenses (user_id, amount, category, description, date, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, description, date, payment_method)
        )
        self.conn.commit()

    def get_recent_expenses(self, user_id, limit=50):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, amount, category, description, date, payment_method
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        return cursor.fetchall()

    def get_expense(self, expense_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, amount, category, description, date, payment_method FROM expenses WHERE id = ?",
            (expense_id,)
        )
        return cursor.fetchone()

    def update_expense(self, expense_id, amount, category, description, date, payment_method):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE expenses
            SET amount = ?, category = ?, description = ?, date = ?, payment_method = ?
            WHERE id = ?
            """,
            (amount, category, description, date, payment_method, expense_id)
        )
        self.conn.commit()

    def delete_expense(self, expense_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

    # ==================================================
    # Date Filtering Operations (Option 1)
    # ==================================================
    def get_filtered_expenses(self, user_id, time_filter="All"):
        cursor = self.conn.cursor()
        today = datetime.now()

        if time_filter == "Today":
            date_str = today.strftime("%d-%m-%Y")
            cursor.execute(
                "SELECT id, amount, category, description, date, payment_method FROM expenses WHERE user_id = ? AND date = ? ORDER BY id DESC",
                (user_id, date_str)
            )
        elif time_filter == "This Month":
            month_str = today.strftime("%m-%Y")
            cursor.execute(
                "SELECT id, amount, category, description, date, payment_method FROM expenses WHERE user_id = ? AND date LIKE ? ORDER BY id DESC",
                (user_id, f"%{month_str}%")
            )
        else:
            return self.get_recent_expenses(user_id)

        return cursor.fetchall()

    # ==================================================
    # Dashboard Metrics
    # ==================================================
    def get_total_expense(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()[0]
        return result if result else 0.0

    def get_month_expense(self, user_id):
        current_month = datetime.now().strftime("%m-%Y")
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date LIKE ?",
            (user_id, f"%{current_month}%")
        )
        result = cursor.fetchone()[0]
        return result if result else 0.0

    def get_total_categories(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT category) FROM expenses WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()[0]
        return result if result else 0

    def search_expenses(self, user_id, query):
        cursor = self.conn.cursor()
        search_pattern = f"%{query}%"
        cursor.execute(
            """
            SELECT id, amount, category, description, date, payment_method
            FROM expenses
            WHERE user_id = ? AND (category LIKE ? OR description LIKE ? OR payment_method LIKE ?)
            ORDER BY date DESC, id DESC
            """,
            (user_id, search_pattern, search_pattern, search_pattern)
        )
        return cursor.fetchall()

    def get_category_breakdown(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category HAVING SUM(amount) > 0",
            (user_id,)
        )
        return cursor.fetchall()

    def get_monthly_spending(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT strftime('%Y-%m', date) as month, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY month ORDER BY month ASC",
            (user_id,)
        )
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows if row[0] is not None}

    def get_all_user_expenses(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT date, category, description, amount, payment_method FROM expenses WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        return cursor.fetchall()