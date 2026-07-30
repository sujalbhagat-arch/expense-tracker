import customtkinter as ctk
from expense import ExpensePage
from edit_expense import EditExpensePage


class Dashboard:

    def __init__(self, app, user):

        self.app = app
        self.user = user

        # ------------------------
        # Main Frame
        # ------------------------
        self.frame = ctk.CTkFrame(
            master=app,
            corner_radius=0
        )
        self.frame.pack(fill="both", expand=True)

        # ------------------------
        # Title
        # ------------------------
        self.title = ctk.CTkLabel(
            self.frame,
            text="💰 Smart Expense Tracker",
            font=("Arial", 30, "bold")
        )
        self.title.pack(pady=(30, 10))

        # ------------------------
        # Welcome Message
        # ------------------------
        self.welcome = ctk.CTkLabel(
            self.frame,
            text=f"Welcome, {user[1]} 👋",
            font=("Arial", 22)
        )
        self.welcome.pack(pady=20)

        # ==================================================
        # Summary Cards
        # ==================================================

        self.cards_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.cards_frame.pack(pady=20)

        # ------------------------
        # Total Expense Card
        # ------------------------
        self.total_card = ctk.CTkFrame(
            self.cards_frame,
            width=180,
            height=100
        )
        self.total_card.grid(row=0, column=0, padx=15)

        self.total_title = ctk.CTkLabel(
            self.total_card,
            text="Total Expense",
            font=("Arial", 16, "bold")
        )
        self.total_title.pack(pady=(15, 5))

        self.total_amount = ctk.CTkLabel(
            self.total_card,
            text=f"₹{self.app.db.get_total_expense(user[0]):.2f}",
            font=("Arial", 24, "bold"),
            text_color="green"
        )
        self.total_amount.pack()

        # ------------------------
        # This Month Card
        # ------------------------
        self.month_card = ctk.CTkFrame(
            self.cards_frame,
            width=180,
            height=100
        )
        self.month_card.grid(row=0, column=1, padx=15)

        self.month_title = ctk.CTkLabel(
            self.month_card,
            text="This Month",
            font=("Arial", 16, "bold")
        )
        self.month_title.pack(pady=(15, 5))

        self.month_amount = ctk.CTkLabel(
            self.month_card,
            text="₹0.00",
            font=("Arial", 24, "bold"),
            text_color="blue"
        )
        self.month_amount.pack()

        # ------------------------
        # Categories Card
        # ------------------------
        self.category_card = ctk.CTkFrame(
            self.cards_frame,
            width=180,
            height=100
        )
        self.category_card.grid(row=0, column=2, padx=15)

        self.category_title = ctk.CTkLabel(
            self.category_card,
            text="Categories",
            font=("Arial", 16, "bold")
        )
        self.category_title.pack(pady=(15, 5))

        self.category_count = ctk.CTkLabel(
            self.category_card,
            text=str(self.app.db.get_total_categories(user[0])),
            font=("Arial", 24, "bold"),
            text_color="orange"
        )
        self.category_count.pack()

        # ==================================================
        # Add Expense Button
        # ==================================================

        self.add_btn = ctk.CTkButton(
            self.frame,
            text="➕ Add Expense",
            width=250,
            height=45,
            command=self.add_expense
        )
        self.add_btn.pack(pady=20)

        # ==================================================
        # Recent Expenses
        # ==================================================

        self.recent_title = ctk.CTkLabel(
            self.frame,
            text="Recent Expenses",
            font=("Arial", 20, "bold")
        )
        self.recent_title.pack(pady=(20, 10))
        # Frame to hold expenses
        self.expense_frame = ctk.CTkFrame(
                self.frame,
                width=700,
                height=180
            )
        self.expense_frame.pack(pady=10)

        # Load expenses
        self.load_recent_expenses()

        # ==================================================
        # Logout Button
        # ==================================================

        self.logout_btn = ctk.CTkButton(
            self.frame,
            text="Logout",
            width=220,
            height=40,
            fg_color="red",
            hover_color="#b30000",
            command=self.logout
        )
        self.logout_btn.pack(pady=40)

    # ------------------------
    # Open Add Expense Window
    # ------------------------
    def add_expense(self):

        popup = ExpensePage(self.app, self.user)

        # Wait until popup closes
        self.app.wait_window(popup.window)

        # Refresh dashboard
        self.refresh_dashboard()
  
        # ------------------------
        # Load Recent Expenses
        # ------------------------
    def load_recent_expenses(self):

        # Clear old widgets
        for widget in self.expense_frame.winfo_children():
            widget.destroy()

        expenses = self.app.db.get_recent_expenses(self.user[0])

        if not expenses:
            label = ctk.CTkLabel(
                self.expense_frame,
                text="No expenses added yet.",
                font=("Arial", 16)
            )
            label.pack(pady=20)
            return

        # Header
        header = ctk.CTkFrame(self.expense_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkLabel(header, text="Date", width=120).grid(row=0, column=0)
        ctk.CTkLabel(header, text="Category", width=150).grid(row=0, column=1)
        ctk.CTkLabel(header, text="Amount", width=100).grid(row=0, column=2)
        ctk.CTkLabel(header, text="Action", width=120).grid(row=0, column=3)

        # Expense Rows
        for expense in expenses:

            expense_id = expense[0]
            amount = expense[1]
            category = expense[2]
            expense_date = expense[3]

            row = ctk.CTkFrame(self.expense_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)

            ctk.CTkLabel(row, text=expense_date, width=120).grid(row=0, column=0)
            ctk.CTkLabel(row, text=category, width=150).grid(row=0, column=1)
            ctk.CTkLabel(row, text=f"₹{amount:.2f}", width=100).grid(row=0, column=2)

            edit_btn = ctk.CTkButton(
               row,
                text="✏ Edit",
                width=70,
                command=lambda eid=expense_id: self.edit_expense(eid)
            )
            edit_btn.grid(row=0, column=3, padx=5)

            delete_btn = ctk.CTkButton(
                row,
                text="🗑 Delete",
                width=70,
                fg_color="red",
                hover_color="#b30000",
                command=lambda eid=expense_id: self.delete_expense(eid)
            )
            delete_btn.grid(row=0, column=4, padx=5)
        # Refresh Dashboard
        # ------------------------
    def refresh_dashboard(self):

        total = self.app.db.get_total_expense(self.user[0])
        self.total_amount.configure(text=f"₹{total:.2f}")

        categories = self.app.db.get_total_categories(self.user[0])
        self.category_count.configure(text=str(categories))

        self.load_recent_expenses()
        # ------------------------
    # Edit Expense
    # ------------------------
    def edit_expense(self, expense_id):

        popup = EditExpensePage(self.app, expense_id)

        self.app.wait_window(popup.window)

        self.refresh_dashboard()
    # ------------------------
    # Delete Expense
    # ------------------------
    def delete_expense(self, expense_id):

        self.app.db.delete_expense(expense_id)

        self.refresh_dashboard()
    # ------------------------
    # Logout Function
    # ------------------------
    def logout(self):

        from login import LoginPage

        self.frame.destroy()
        LoginPage(self.app)