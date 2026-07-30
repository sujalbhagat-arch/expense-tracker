import customtkinter as ctk
from expense import ExpensePage


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
            text="₹0.00",
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
            text="0",
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

        self.no_expense = ctk.CTkLabel(
            self.frame,
            text="No expenses added yet.",
            font=("Arial", 16)
        )
        self.no_expense.pack()

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
        ExpensePage(self.app, self.user)

    # ------------------------
    # Logout Function
    # ------------------------
    def logout(self):

        from login import LoginPage

        self.frame.destroy()
        LoginPage(self.app)