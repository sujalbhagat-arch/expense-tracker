import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime
from charts import AnalyticsPage
from edit_expense import EditExpensePage


class Dashboard:

    def __init__(self, app, user):
        self.app = app
        self.user = user
        self.app.current_dashboard = self

        # Setup Container
        self.frame = ctk.CTkFrame(app)
        self.frame.pack(fill="both", expand=True)

        # Header Section
        self.header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=10)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="💰 Smart Expense Tracker",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(side="left")

        # Theme Switcher
        self.theme_btn = ctk.CTkButton(
            self.header_frame,
            text="🌙/☀️ Switch Theme",
            width=120,
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right")

        # Welcome Text
        self.welcome_label = ctk.CTkLabel(
            self.frame,
            text=f"Welcome back, {self.user[1]} 👋",
            font=("Arial", 16)
        )
        self.welcome_label.pack(pady=(0, 10))

        # Metrics Cards Frame
        self.cards_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=20, pady=5)
        self.cards_frame.columnconfigure((0, 1, 2), weight=1)

        # Card 1: Total Spent
        self.card_total = ctk.CTkFrame(self.cards_frame, corner_radius=10)
        self.card_total.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.card_total, text="Total Expense", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.total_val = ctk.CTkLabel(self.card_total, text="₹0.00", font=("Arial", 18, "bold"), text_color="#2ecc71")
        self.total_val.pack(pady=(5, 10))

        # Card 2: This Month
        self.card_month = ctk.CTkFrame(self.cards_frame, corner_radius=10)
        self.card_month.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.card_month, text="This Month", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.month_val = ctk.CTkLabel(self.card_month, text="₹0.00", font=("Arial", 18, "bold"), text_color="#3498db")
        self.month_val.pack(pady=(5, 10))

        # Card 3: Categories
        self.card_cat = ctk.CTkFrame(self.cards_frame, corner_radius=10)
        self.card_cat.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.card_cat, text="Categories", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.cat_val = ctk.CTkLabel(self.card_cat, text="0", font=("Arial", 18, "bold"), text_color="#e67e22")
        self.cat_val.pack(pady=(5, 10))

        # ==================================================
        # Monthly Budget Progress Card
        # ==================================================
        self.budget_card = ctk.CTkFrame(self.frame, corner_radius=10)
        self.budget_card.pack(fill="x", padx=30, pady=10)

        self.budget_header_frame = ctk.CTkFrame(self.budget_card, fg_color="transparent")
        self.budget_header_frame.pack(fill="x", padx=15, pady=(10, 5))

        self.budget_status_lbl = ctk.CTkLabel(
            self.budget_header_frame,
            text="Monthly Budget: ₹0.00 / ₹0.00",
            font=("Arial", 13, "bold")
        )
        self.budget_status_lbl.pack(side="left")

        self.set_budget_btn = ctk.CTkButton(
            self.budget_header_frame,
            text="⚙️ Set Budget",
            width=100,
            height=26,
            fg_color="#8e44ad",
            hover_color="#732d91",
            command=self.prompt_set_budget
        )
        self.set_budget_btn.pack(side="right")

        self.budget_progress = ctk.CTkProgressBar(self.budget_card, height=12)
        self.budget_progress.pack(fill="x", padx=15, pady=(0, 10))
        self.budget_progress.set(0)

        # Action Buttons Section
        self.action_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.action_frame.pack(pady=10)

        self.add_btn = ctk.CTkButton(
            self.action_frame,
            text="➕ Add Expense",
            command=self.open_add_expense_modal
        )
        self.add_btn.grid(row=0, column=0, padx=10)

        self.analytics_btn = ctk.CTkButton(
            self.action_frame,
            text="📊 Analytics & Charts",
            fg_color="#8e44ad",
            hover_color="#732d91",
            command=self.open_analytics
        )
        self.analytics_btn.grid(row=0, column=1, padx=10)

        # Search Bar Section
        self.search_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="🔍 Search expenses by category or description...",
            width=500
        )
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Recent Expenses Title
        ctk.CTkLabel(self.frame, text="Recent Expenses", font=("Arial", 16, "bold")).pack(pady=5)

        # Expenses Scrollable Table
        self.expenses_scroll = ctk.CTkScrollableFrame(self.frame, height=220)
        self.expenses_scroll.pack(fill="both", expand=True, padx=30, pady=5)

        # Logout Button
        self.logout_btn = ctk.CTkButton(
            self.frame,
            text="Logout",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.logout
        )
        self.logout_btn.pack(pady=10)

        # Initial Load
        self.update_metrics()
        self.load_expenses()

    # --------------------------------------------------
    # Budget Logic
    # --------------------------------------------------
    def prompt_set_budget(self):
        current_budget = self.app.db.get_user_budget(self.user[0])
        new_budget = simpledialog.askfloat(
            "Set Monthly Budget",
            "Enter your target monthly budget limit (INR):",
            initialvalue=current_budget,
            minvalue=0.0
        )

        if new_budget is not None:
            self.app.db.set_user_budget(self.user[0], new_budget)
            messagebox.showinfo("Success", f"Monthly budget set to ₹{new_budget:.2f}")
            self.update_metrics()

    def update_metrics(self):
        total = self.app.db.get_total_expense(self.user[0])
        month = self.app.db.get_month_expense(self.user[0])
        categories = self.app.db.get_total_categories(self.user[0])
        budget = self.app.db.get_user_budget(self.user[0])

        self.total_val.configure(text=f"₹{total:.2f}")
        self.month_val.configure(text=f"₹{month:.2f}")
        self.cat_val.configure(text=str(categories))

        # Update Budget Status Card
        if budget > 0:
            percentage = min(month / budget, 1.0)
            self.budget_progress.set(percentage)
            remaining = budget - month

            if month >= budget:
                self.budget_status_lbl.configure(
                    text=f"⚠️ Budget Exceeded! spent ₹{month:.2f} of ₹{budget:.2f} (Over by ₹{abs(remaining):.2f})",
                    text_color="#e74c3c"
                )
                self.budget_progress.configure(progress_color="#e74c3c")
            elif percentage >= 0.75:
                self.budget_status_lbl.configure(
                    text=f"⚠️ Near Budget Limit: spent ₹{month:.2f} of ₹{budget:.2f} (₹{remaining:.2f} left)",
                    text_color="#f39c12"
                )
                self.budget_progress.configure(progress_color="#f39c12")
            else:
                self.budget_status_lbl.configure(
                    text=f"Monthly Budget: spent ₹{month:.2f} of ₹{budget:.2f} (₹{remaining:.2f} left)",
                    text_color="#2ecc71"
                )
                self.budget_progress.configure(progress_color="#2ecc71")
        else:
            self.budget_status_lbl.configure(
                text="Monthly Budget: Not Set (Click Set Budget to configure)",
                text_color="white"
            )
            self.budget_progress.set(0)
            self.budget_progress.configure(progress_color="#3498db")

    # --------------------------------------------------
    # Expenses Rendering & Actions
    # --------------------------------------------------
    def load_expenses(self, expenses=None):
        for widget in self.expenses_scroll.winfo_children():
            widget.destroy()

        if expenses is None:
            expenses = self.app.db.get_recent_expenses(self.user[0])

        if not expenses:
            ctk.CTkLabel(self.expenses_scroll, text="No expenses found.").pack(pady=20)
            return

        headers_frame = ctk.CTkFrame(self.expenses_scroll, fg_color="transparent")
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(headers_frame, text="Date", font=("Arial", 12, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(headers_frame, text="Category", font=("Arial", 12, "bold")).grid(row=0, column=1)
        ctk.CTkLabel(headers_frame, text="Amount", font=("Arial", 12, "bold")).grid(row=0, column=2)
        ctk.CTkLabel(headers_frame, text="Actions", font=("Arial", 12, "bold")).grid(row=0, column=3)

        for exp in expenses:
            exp_id, amount, category, desc, date = exp
            row = ctk.CTkFrame(self.expenses_scroll)
            row.pack(fill="x", pady=2)
            row.columnconfigure((0, 1, 2, 3), weight=1)

            ctk.CTkLabel(row, text=str(date)).grid(row=0, column=0, padx=5, pady=5)
            ctk.CTkLabel(row, text=str(category)).grid(row=0, column=1, padx=5, pady=5)
            ctk.CTkLabel(row, text=f"₹{amount:.2f}").grid(row=0, column=2, padx=5, pady=5)

            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.grid(row=0, column=3, padx=5, pady=5)

            edit_btn = ctk.CTkButton(
                actions_frame,
                text="✏️ Edit",
                width=60,
                height=24,
                command=lambda e_id=exp_id: self.edit_expense(e_id)
            )
            edit_btn.pack(side="left", padx=2)

            del_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️ Delete",
                width=60,
                height=24,
                fg_color="#e74c3c",
                hover_color="#c0392b",
                command=lambda e_id=exp_id: self.delete_expense(e_id)
            )
            del_btn.pack(side="left", padx=2)

    def on_search(self, event):
        query = self.search_entry.get().strip()
        if query:
            results = self.app.db.search_expenses(self.user[0], query)
            self.load_expenses(results)
        else:
            self.load_expenses()

    def open_add_expense_modal(self):
        modal = ctk.CTkToplevel(self.app)
        modal.title("Add New Expense")
        modal.geometry("380x420")
        modal.grab_set()

        ctk.CTkLabel(modal, text="Add Expense", font=("Arial", 18, "bold")).pack(pady=15)

        amount_entry = ctk.CTkEntry(modal, placeholder_text="Amount (INR)", width=280)
        amount_entry.pack(pady=8)

        category_entry = ctk.CTkEntry(modal, placeholder_text="Category (e.g. Food, Travel)", width=280)
        category_entry.pack(pady=8)

        desc_entry = ctk.CTkEntry(modal, placeholder_text="Description (Optional)", width=280)
        desc_entry.pack(pady=8)

        today_str = datetime.now().strftime("%d-%m-%Y")
        date_entry = ctk.CTkEntry(modal, width=280)
        date_entry.insert(0, today_str)
        date_entry.pack(pady=8)

        def save():
            try:
                amt = float(amount_entry.get().strip())
                cat = category_entry.get().strip()
                desc = desc_entry.get().strip()
                dt = date_entry.get().strip()

                if not amt or not cat or not dt:
                    messagebox.showerror("Error", "Amount, Category, and Date are required!")
                    return

                datetime.strptime(dt, "%d-%m-%Y")

                self.app.db.add_expense(self.user[0], amt, cat, desc, dt)
                messagebox.showinfo("Success", "Expense added!")
                modal.destroy()
                self.update_metrics()
                self.load_expenses()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount or date format (DD-MM-YYYY)!")

        ctk.CTkButton(modal, text="Save Expense", command=save).pack(pady=15)

    def edit_expense(self, expense_id):
        EditExpensePage(self.app, expense_id)

    def delete_expense(self, expense_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?"):
            self.app.db.delete_expense(expense_id)
            self.update_metrics()
            self.load_expenses()

    def open_analytics(self):
        AnalyticsPage(self.app, self.user)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    def logout(self):
        from login import LoginPage
        self.frame.destroy()
        LoginPage(self.app)