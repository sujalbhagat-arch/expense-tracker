import sqlite3


class Database:

    def __init__(self, db_file="expense_tracker.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Users Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                budget REAL DEFAULT 0.0,
                profile_pic TEXT
            )
        ''')

        # Expenses Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                category TEXT,
                description TEXT,
                date TEXT,
                payment_method TEXT DEFAULT 'UPI',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        # Category Budgets Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS category_budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                limit_amount REAL,
                UNIQUE(user_id, category)
            )
        ''')

        self.conn.commit()

        # Schema Migrations (Ensures older DB files seamlessly get new columns)
        self._run_migrations()

    def _run_migrations(self):
        # Migrate profile_pic column
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN profile_pic TEXT")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists

        # Migrate payment_method column
        try:
            self.cursor.execute("ALTER TABLE expenses ADD COLUMN payment_method TEXT DEFAULT 'UPI'")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists

        # Check and fix category_budgets table if limit_amount is missing
        try:
            self.cursor.execute("SELECT limit_amount FROM category_budgets LIMIT 1")
        except sqlite3.OperationalError:
            self.cursor.execute("DROP TABLE IF EXISTS category_budgets")
            self.cursor.execute('''
                CREATE TABLE category_budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    category TEXT,
                    limit_amount REAL,
                    UNIQUE(user_id, category)
                )
            ''')
            self.conn.commit()

    # ==========================================
    # USER & PROFILE OPERATIONS
    # ==========================================
    def register_user(self, username, password, *args, **kwargs):
        """
        Registers a new user into the DB.
        *args and **kwargs safely handle extra parameters (e.g. confirm_password, email)
        passed by any register window without breaking.
        """
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", 
                (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def add_user(self, username, password, *args, **kwargs):
        """Alias for register_user to support older/alternative registration logic."""
        return self.register_user(username, password, *args, **kwargs)

    def login_user(self, username, password):
        self.cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?", 
            (username, password)
        )
        return self.cursor.fetchone()

    def validate_user(self, username, password):
        """Alias for login_user authentication."""
        return self.login_user(username, password)

    def update_user_profile_pic(self, user_id, image_path):
        self.cursor.execute("UPDATE users SET profile_pic = ? WHERE id = ?", (image_path, user_id))
        self.conn.commit()

    def get_user_profile_pic(self, user_id):
        self.cursor.execute("SELECT profile_pic FROM users WHERE id = ?", (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res else None

    # ==========================================
    # BUDGET OPERATIONS
    # ==========================================
    def set_user_budget(self, user_id, budget_amount):
        self.cursor.execute("UPDATE users SET budget = ? WHERE id = ?", (budget_amount, user_id))
        self.conn.commit()

    def get_user_budget(self, user_id):
        self.cursor.execute("SELECT budget FROM users WHERE id = ?", (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res and res[0] else 0.0

    def set_category_budget(self, user_id, category, limit_amount):
        self.cursor.execute('''
            INSERT INTO category_budgets (user_id, category, limit_amount)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, category) DO UPDATE SET limit_amount = excluded.limit_amount
        ''', (user_id, category, limit_amount))
        self.conn.commit()

    def get_category_budgets(self, user_id):
        try:
            self.cursor.execute("SELECT category, limit_amount FROM category_budgets WHERE user_id = ?", (user_id,))
            rows = self.cursor.fetchall()
            return {row[0]: row[1] for row in rows}
        except sqlite3.OperationalError:
            return {}

    def get_category_month_spending(self, user_id, category):
        self.cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE user_id = ? AND category = ? AND strftime('%m-%Y', substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) = strftime('%m-%Y', 'now')
        ''', (user_id, category))
        res = self.cursor.fetchone()
        return res[0] if res and res[0] else 0.0

    # ==========================================
    # EXPENSE OPERATIONS
    # ==========================================
    def add_expense(self, user_id, amount, category, description, date, payment_method="UPI"):
        self.cursor.execute('''
            INSERT INTO expenses (user_id, amount, category, description, date, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, amount, category, description, date, payment_method))
        self.conn.commit()

    def get_expense(self, expense_id):
        self.cursor.execute("SELECT id, amount, category, description, date, payment_method FROM expenses WHERE id = ?", (expense_id,))
        return self.cursor.fetchone()

    def update_expense(self, expense_id, amount, category, description, date, payment_method):
        self.cursor.execute('''
            UPDATE expenses 
            SET amount = ?, category = ?, description = ?, date = ?, payment_method = ?
            WHERE id = ?
        ''', (amount, category, description, date, payment_method, expense_id))
        self.conn.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

    def get_filtered_expenses(self, user_id, filter_mode="All"):
        if filter_mode == "Today":
            self.cursor.execute('''
                SELECT id, amount, category, description, date, payment_method 
                FROM expenses WHERE user_id = ? 
                AND strftime('%d-%m-%Y', substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) = strftime('%d-%m-%Y', 'now')
                ORDER BY id DESC
            ''', (user_id,))
        elif filter_mode == "This Month":
            self.cursor.execute('''
                SELECT id, amount, category, description, date, payment_method 
                FROM expenses WHERE user_id = ? 
                AND strftime('%m-%Y', substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) = strftime('%m-%Y', 'now')
                ORDER BY id DESC
            ''', (user_id,))
        else:
            self.cursor.execute('''
                SELECT id, amount, category, description, date, payment_method 
                FROM expenses WHERE user_id = ? ORDER BY id DESC
            ''', (user_id,))
        return self.cursor.fetchall()

    def search_expenses(self, user_id, query):
        q = f"%{query}%"
        self.cursor.execute('''
            SELECT id, amount, category, description, date, payment_method 
            FROM expenses 
            WHERE user_id = ? AND (category LIKE ? OR description LIKE ? OR payment_method LIKE ?)
            ORDER BY id DESC
        ''', (user_id, q, q, q))
        return self.cursor.fetchall()

    # ==========================================
    # METRICS & STATS FOR ANALYTICS
    # ==========================================
    def get_category_breakdown(self, user_id):
        self.cursor.execute('''
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = ? 
            GROUP BY category
        ''', (user_id,))
        rows = self.cursor.fetchall()
        return {row[0]: row[1] for row in rows}

    def get_total_expense(self, user_id):
        self.cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res and res[0] else 0.0

    def get_month_expense(self, user_id):
        self.cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE user_id = ? 
            AND strftime('%m-%Y', substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) = strftime('%m-%Y', 'now')
        ''', (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res and res[0] else 0.0

    def get_total_categories(self, user_id):
        self.cursor.execute("SELECT COUNT(DISTINCT category) FROM expenses WHERE user_id = ?", (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res else 0