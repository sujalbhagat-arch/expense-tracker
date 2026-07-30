import customtkinter as ctk
from expense import ExpensePage
from edit_expense import EditExpensePage


class Dashboard:

    def __init__(self, app, user):

        self.app = app
        self.user = user

        # ------------------------
        # Main Scrollable Frame
        # ------------------------
        self.frame = ctk.CTkScrollableFrame(
            master=app,
            corner_radius=0
        )
        self.frame.pack(fill="both", expand=True)

        # ------------------------
        # Header Bar (Title + Theme Toggle)
        # ------------------------
        self.header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 0))

        self.title = ctk.CTkLabel(
            self.header_frame,
            text="💰 Smart Expense Tracker",
            font=("Arial", 28, "bold")
        )
        self.title.pack(side="left")

        # Theme Toggle Button
        self.theme_btn = ctk.CTkButton(
            self.header_frame,
            text="🌙 / ☀️ Switch Theme",
            width=120,
            height=30,
            fg_color="gray",
            hover_color="#555555",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right")

        # Welcome Message
        self.welcome = ctk.CTkLabel(
            self.frame,
            text=f"Welcome back, {user[1]} 👋",
            font=("Arial", 18)
        )
        self.welcome.pack(pady=(10, 15))

        # ==================================================
        # Summary Cards
        # ==================================================
        self.cards_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.cards_frame.pack(pady=10)

        # Total Expense Card
        self.total_card = ctk.CTkFrame(self.cards_frame, width=180, height=90)
        self.total_card.grid(row=0, column=0, padx=10)
        ctk.CTkLabel(self.total_card, text="Total Expense", font=("Arial", 14, "bold")).pack(pady=(10, 2))
        self.total_amount = ctk.CTkLabel(
            self.total_card,
            text=f"₹{self.app.db.get_total_expense(user[0]):.2f}",
            font=("Arial", 20, "bold"),
            text_color="#2ecc71"
        )
        self.total_amount.pack()

        # This Month Card
        self.month_card = ctk.CTkFrame(self.cards_frame, width=180, height=90)
        self.month_card.grid(row=0, column=1, padx=10)
        ctk.CTkLabel(self.month_card, text="This Month", font=("Arial", 14, "bold")).pack(pady=(10, 2))
        self.month_amount = ctk.CTkLabel(
            self.month_card,
            text=f"₹{self.app.db.get_month_expense(user[0]):.2f}",
            font=("Arial", 20, "bold"),
            text_color="#3498db"
        )
        self.month_amount.pack()

        # Categories Card
        self.category_card = ctk.CTkFrame(self.cards_frame, width=180, height=90)
        self.category_card.grid(row=0, column=2, padx=10)
        ctk.CTkLabel(self.category_card, text="Categories", font=("Arial", 14, "bold")).pack(pady=(10, 2))
        self.category_count = ctk.CTkLabel(
            self.category_card,
            text=str(self.app.db.get_total_categories(user[0])),
            font=("Arial", 20, "bold"),
            text_color="#e67e22"
        )
        self.category_count.pack()

        # ==================================================
        # Action Buttons
        # ==================================================
        self.action_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.action_frame.pack(pady=15)

        self.add_btn = ctk.CTkButton(
            self.action_frame,
            text="➕ Add Expense",
            width=200,
            height=40,
            command=self.add_expense
        )
        self.add_btn.grid(row=0, column=0, padx=10)

        self.analytics_btn = ctk.CTkButton(
            self.action_frame,
            text="📊 Analytics & Charts",
            width=200,
            height=40,
            fg_color="#8e44ad",
            hover_color="#732d91",
            command=self.open_analytics
        )
        self.analytics_btn.grid(row=0, column=1, padx=10)

        # ==================================================
        # Search Bar
        # ==================================================
        self.search_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.search_frame.pack(pady=(15, 5))

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Search expenses by category or description...",
            width=450,
            height=35
        )
        self.search_entry.pack(side="left", padx=5)
        # Dynamic search trigger on key release
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # ==================================================
        # Expense List Frame
        # ==================================================
        self.recent_title = ctk.CTkLabel(
            self.frame,
            text="Recent Expenses",
            font=("Arial", 20, "bold")
        )
        self.recent_title.pack(pady=(15, 5))

        self.expense_frame = ctk.CTkFrame(self.frame, width=750)
        self.expense_frame.pack(pady=10)

        # Initial Load
        self.load_expenses()

        # ==================================================
        # Logout Button
        # ==================================================
        self.logout_btn = ctk.CTkButton(
            self.frame,
            text="Logout",
            width=200,
            height=35,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.logout
        )
        self.logout_btn.pack(pady=20)

    # ------------------------
    # Live Search Handler
    # ------------------------
    def on_search(self, event=None):
        query = self.search_entry.get().strip()
        if query:
            results = self.app.db.search_expenses(self.user[0], query)
            self.render_expense_list(results)
        else:
            self.load_expenses()

    # ------------------------
    # Load & Render Methods
    # ------------------------
    def load_expenses(self):
        expenses = self.app.db.get_recent_expenses(self.user[0])
        self.render_expense_list(expenses)

    def render_expense_list(self, expenses):
        for widget in self.expense_frame.winfo_children():
            widget.destroy()

        if not expenses:
            label = ctk.CTkLabel(
                self.expense_frame,
                text="No matching expenses found.",
                font=("Arial", 14)
            )
            label.pack(pady=20)
            return

        header = ctk.CTkFrame(self.expense_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkLabel(header, text="Date", width=110, font=("Arial", 12, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(header, text="Category", width=130, font=("Arial", 12, "bold")).grid(row=0, column=1)
        ctk.CTkLabel(header, text="Amount", width=100, font=("Arial", 12, "bold")).grid(row=0, column=2)
        ctk.CTkLabel(header, text="Actions", width=140, font=("Arial", 12, "bold")).grid(row=0, column=3, columnspan=2)

        for expense in expenses:
            expense_id = expense[0]
            amount = expense[1]
            category = expense[2]
            expense_date = expense[3 if len(expense) <= 4 else 4]

            row = ctk.CTkFrame(self.expense_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=3)

            ctk.CTkLabel(row, text=expense_date, width=110).grid(row=0, column=0)
            ctk.CTkLabel(row, text=category, width=130).grid(row=0, column=1)
            ctk.CTkLabel(row, text=f"₹{amount:.2f}", width=100).grid(row=0, column=2)

            edit_btn = ctk.CTkButton(
                row,
                text="✏ Edit",
                width=65,
                height=25,
                command=lambda eid=expense_id: self.edit_expense(eid)
            )
            edit_btn.grid(row=0, column=3, padx=3)

            delete_btn = ctk.CTkButton(
                row,
                text="🗑 Delete",
                width=65,
                height=25,
                fg_color="#e74c3c",
                hover_color="#c0392b",
                command=lambda eid=expense_id: self.delete_expense(eid)
            )
            delete_btn.grid(row=0, column=4, padx=3)

    # ------------------------
    # Helpers
    # ------------------------
    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def open_analytics(self):
        print("Analytics clicked!")

    def add_expense(self):
        popup = ExpensePage(self.app, self.user)
        self.app.wait_window(popup.window)
        self.refresh_dashboard()

    def refresh_dashboard(self):
        total = self.app.db.get_total_expense(self.user[0])
        self.total_amount.configure(text=f"₹{total:.2f}")

        month_total = self.app.db.get_month_expense(self.user[0])
        self.month_amount.configure(text=f"₹{month_total:.2f}")

        categories = self.app.db.get_total_categories(self.user[0])
        self.category_count.configure(text=str(categories))

        self.on_search()

    def edit_expense(self, expense_id):
        popup = EditExpensePage(self.app, expense_id)
        self.app.wait_window(popup.window)
        self.refresh_dashboard()

    def delete_expense(self, expense_id):
        self.app.db.delete_expense(expense_id)
        self.refresh_dashboard()

    def logout(self):
        from login import LoginPage
        self.frame.destroy()
        LoginPage(self.app)