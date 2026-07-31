import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog
from datetime import datetime
import os
from PIL import Image

from charts import AnalyticsPage
from edit_expense import EditExpensePage


class Dashboard:

    def __init__(self, app, user):
        self.app = app
        self.user = user
        self.app.current_dashboard = self

        # Theme Color Palette Tuple (Light Mode Color, Dark Mode Color)
        self.bg_color = ("#f4f4f5", "#18181b")
        self.card_bg = ("#ffffff", "#27272a")
        self.card_border = ("#e4e4e7", "#3f3f46")
        self.text_primary = ("#18181b", "#f4f4f5")
        self.text_secondary = ("#71717a", "#a1a1aa")

        # Main Container
        self.frame = ctk.CTkFrame(app, fg_color=self.bg_color)
        self.frame.pack(fill="both", expand=True)

        # ==========================================
        # TOP HEADER
        # ==========================================
        self.header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=25, pady=(15, 5))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="💳 Smart Expense Tracker",
            font=("Arial", 22, "bold"),
            text_color=self.text_primary
        )
        self.title_label.pack(side="left")

        # Right Side Header Actions
        self.header_right = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_right.pack(side="right")

        # Profile Photo Avatar Button
        self.avatar_btn = ctk.CTkButton(
            self.header_right,
            text="👤",
            width=40,
            height=40,
            corner_radius=20,
            fg_color=self.card_border,
            hover_color=("#d4d4d8", "#52525b"),
            command=self.change_profile_photo
        )
        self.avatar_btn.pack(side="left", padx=(0, 10))

        self.welcome_label = ctk.CTkLabel(
            self.header_right,
            text=f"Welcome, {self.user[1]} 👋",
            font=("Arial", 13, "bold"),
            text_color=self.text_secondary
        )
        self.welcome_label.pack(side="left", padx=(0, 15))

        self.theme_btn = ctk.CTkButton(
            self.header_right,
            text="🌙/☀️ Theme",
            width=90,
            height=30,
            corner_radius=8,
            fg_color=self.card_bg,
            hover_color=self.card_border,
            text_color=self.text_primary,
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="left")

        self.load_profile_photo()

        # ==========================================
        # METRICS CARDS ROW
        # ==========================================
        self.cards_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=20, pady=10)
        self.cards_frame.columnconfigure((0, 1, 2), weight=1)

        # Card 1: Total Spent
        self.card_total = ctk.CTkFrame(self.cards_frame, fg_color=self.card_bg, corner_radius=14, border_width=1, border_color=self.card_border)
        self.card_total.grid(row=0, column=0, padx=8, pady=5, sticky="ew")
        ctk.CTkLabel(self.card_total, text="Total Expenses", font=("Arial", 12), text_color=self.text_secondary).pack(anchor="w", padx=15, pady=(12, 0))
        self.total_val = ctk.CTkLabel(self.card_total, text="₹0.00", font=("Arial", 20, "bold"), text_color="#16a34a")
        self.total_val.pack(anchor="w", padx=15, pady=(2, 12))

        # Card 2: This Month
        self.card_month = ctk.CTkFrame(self.cards_frame, fg_color=self.card_bg, corner_radius=14, border_width=1, border_color=self.card_border)
        self.card_month.grid(row=0, column=1, padx=8, pady=5, sticky="ew")
        ctk.CTkLabel(self.card_month, text="This Month", font=("Arial", 12), text_color=self.text_secondary).pack(anchor="w", padx=15, pady=(12, 0))
        self.month_val = ctk.CTkLabel(self.card_month, text="₹0.00", font=("Arial", 20, "bold"), text_color="#2563eb")
        self.month_val.pack(anchor="w", padx=15, pady=(2, 12))

        # Card 3: Categories
        self.card_cat = ctk.CTkFrame(self.cards_frame, fg_color=self.card_bg, corner_radius=14, border_width=1, border_color=self.card_border)
        self.card_cat.grid(row=0, column=2, padx=8, pady=5, sticky="ew")
        ctk.CTkLabel(self.card_cat, text="Categories Used", font=("Arial", 12), text_color=self.text_secondary).pack(anchor="w", padx=15, pady=(12, 0))
        self.cat_val = ctk.CTkLabel(self.card_cat, text="0", font=("Arial", 20, "bold"), text_color="#ea580c")
        self.cat_val.pack(anchor="w", padx=15, pady=(2, 12))

        # ==========================================
        # BUDGET PROGRESS CARD
        # ==========================================
        self.budget_card = ctk.CTkFrame(self.frame, fg_color=self.card_bg, corner_radius=14, border_width=1, border_color=self.card_border)
        self.budget_card.pack(fill="x", padx=28, pady=5)

        self.budget_header = ctk.CTkFrame(self.budget_card, fg_color="transparent")
        self.budget_header.pack(fill="x", padx=15, pady=(10, 4))

        self.budget_status_lbl = ctk.CTkLabel(
            self.budget_header,
            text="Monthly Budget: ₹0.00 / ₹0.00",
            font=("Arial", 13, "bold"),
            text_color=self.text_primary
        )
        self.budget_status_lbl.pack(side="left")

        self.cat_budget_btn = ctk.CTkButton(
            self.budget_header,
            text="🏷️ Category Limits",
            width=120,
            height=28,
            corner_radius=8,
            fg_color="#0d9488",
            hover_color="#0f766e",
            command=self.open_category_budget_modal
        )
        self.cat_budget_btn.pack(side="right", padx=(5, 0))

        self.set_budget_btn = ctk.CTkButton(
            self.budget_header,
            text="⚙️ Set Budget",
            width=100,
            height=28,
            corner_radius=8,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.prompt_set_budget
        )
        self.set_budget_btn.pack(side="right")

        self.budget_progress = ctk.CTkProgressBar(self.budget_card, height=10, corner_radius=5)
        self.budget_progress.pack(fill="x", padx=15, pady=(0, 12))
        self.budget_progress.set(0)

        # ==========================================
        # ACTION BUTTONS & SEARCH BAR
        # ==========================================
        self.middle_bar = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.middle_bar.pack(fill="x", padx=28, pady=10)

        self.add_btn = ctk.CTkButton(
            self.middle_bar,
            text="➕ Add Expense",
            font=("Arial", 13, "bold"),
            height=36,
            corner_radius=8,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.open_add_expense_modal
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        self.analytics_btn = ctk.CTkButton(
            self.middle_bar,
            text="📊 Analytics & Charts",
            font=("Arial", 13, "bold"),
            height=36,
            corner_radius=8,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.open_analytics
        )
        self.analytics_btn.pack(side="left", padx=(0, 15))

        self.search_entry = ctk.CTkEntry(
            self.middle_bar,
            placeholder_text="🔍 Search expenses, categories, payment methods...",
            height=36,
            corner_radius=8,
            border_width=1,
            border_color=self.card_border
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.date_filter_menu = ctk.CTkOptionMenu(
            self.middle_bar,
            values=["All", "Today", "This Month"],
            width=110,
            height=36,
            corner_radius=8,
            fg_color=self.card_bg,
            button_color=self.card_border,
            text_color=self.text_primary,
            command=self.on_filter_change
        )
        self.date_filter_menu.set("All")
        self.date_filter_menu.pack(side="right")

        # ==========================================
        # TABLE VIEW
        # ==========================================
        self.expenses_scroll = ctk.CTkScrollableFrame(
            self.frame,
            fg_color=self.bg_color,
            corner_radius=10
        )
        self.expenses_scroll.pack(fill="both", expand=True, padx=28, pady=(0, 10))

        # Logout Button
        self.logout_btn = ctk.CTkButton(
            self.frame,
            text="Logout",
            fg_color="#dc2626",
            hover_color="#b91c1c",
            height=30,
            width=100,
            corner_radius=8,
            command=self.logout
        )
        self.logout_btn.pack(pady=(0, 10))

        # Initial Refresh
        self.update_metrics()
        self.load_expenses()

    # --------------------------------------------------
    # Profile Photo Management
    # --------------------------------------------------
    def change_profile_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")]
        )
        if file_path:
            self.app.db.update_user_profile_pic(self.user[0], file_path)
            self.load_profile_photo(file_path)

    def load_profile_photo(self, path=None):
        if not path:
            path = self.app.db.get_user_profile_pic(self.user[0])

        if path and os.path.exists(path):
            try:
                img = Image.open(path).resize((40, 40), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
                self.avatar_btn.configure(image=ctk_img, text="")
            except Exception as e:
                print("Error loading profile picture:", e)

    # --------------------------------------------------
    # Budget Operations & Alerts
    # --------------------------------------------------
    def prompt_set_budget(self):
        current_budget = self.app.db.get_user_budget(self.user[0])
        new_budget = simpledialog.askfloat(
            "Overall Budget Limit",
            "Set monthly overall budget limit (₹):",
            initialvalue=current_budget,
            minvalue=0.0
        )
        if new_budget is not None:
            self.app.db.set_user_budget(self.user[0], new_budget)
            messagebox.showinfo("Success", f"Monthly budget set to ₹{new_budget:.2f}")
            self.update_metrics()

    def open_category_budget_modal(self):
        modal = ctk.CTkToplevel(self.app)
        modal.title("Manage Category Budgets")
        modal.geometry("380x300")
        modal.grab_set()

        ctk.CTkLabel(modal, text="Category Budgets", font=("Arial", 18, "bold")).pack(pady=12)

        cat_entry = ctk.CTkEntry(modal, placeholder_text="Category (e.g. Food)", width=260, height=36)
        cat_entry.pack(pady=8)

        limit_entry = ctk.CTkEntry(modal, placeholder_text="Monthly Limit (₹)", width=260, height=36)
        limit_entry.pack(pady=8)

        def save_cat_budget():
            cat = cat_entry.get().strip()
            try:
                amt = float(limit_entry.get().strip())
                if not cat or amt <= 0:
                    messagebox.showerror("Error", "Enter valid category and limit.")
                    return
                self.app.db.set_category_budget(self.user[0], cat, amt)
                messagebox.showinfo("Saved", f"Budget for {cat} set to ₹{amt:.2f}")
                modal.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid numeric limit.")

        ctk.CTkButton(modal, text="Save Limit", height=36, fg_color="#0d9488", command=save_cat_budget).pack(pady=15)

    def check_over_budget_alerts(self, new_expense_amount, category):
        overall_budget = self.app.db.get_user_budget(self.user[0])
        month_spent = self.app.db.get_month_expense(self.user[0]) + new_expense_amount

        if overall_budget > 0 and month_spent > overall_budget:
            messagebox.showwarning(
                "🚨 Overall Budget Exceeded!",
                f"This expense puts your monthly spending at ₹{month_spent:.2f}, exceeding your limit of ₹{overall_budget:.2f}!"
            )

        cat_budgets = self.app.db.get_category_budgets(self.user[0])
        if category in cat_budgets:
            cat_limit = cat_budgets[category]
            cat_spent = self.app.db.get_category_month_spending(self.user[0], category) + new_expense_amount
            if cat_spent > cat_limit:
                messagebox.showwarning(
                    "🚨 Category Budget Exceeded!",
                    f"Spending on '{category}' will reach ₹{cat_spent:.2f}, exceeding its limit of ₹{cat_limit:.2f}!"
                )

    def update_metrics(self):
        total = self.app.db.get_total_expense(self.user[0])
        month = self.app.db.get_month_expense(self.user[0])
        categories = self.app.db.get_total_categories(self.user[0])
        budget = self.app.db.get_user_budget(self.user[0])

        self.total_val.configure(text=f"₹{total:.2f}")
        self.month_val.configure(text=f"₹{month:.2f}")
        self.cat_val.configure(text=str(categories))

        if budget > 0:
            percentage = min(month / budget, 1.0)
            self.budget_progress.set(percentage)
            remaining = budget - month

            if month >= budget:
                self.budget_status_lbl.configure(
                    text=f"⚠️ Budget Exceeded: spent ₹{month:.2f} of ₹{budget:.2f} (+₹{abs(remaining):.2f})",
                    text_color="#ef4444"
                )
                self.budget_progress.configure(progress_color="#ef4444")
            elif percentage >= 0.75:
                self.budget_status_lbl.configure(
                    text=f"⚠️ Near Limit: spent ₹{month:.2f} of ₹{budget:.2f} (₹{remaining:.2f} left)",
                    text_color="#f59e0b"
                )
                self.budget_progress.configure(progress_color="#f59e0b")
            else:
                self.budget_status_lbl.configure(
                    text=f"Monthly Budget: spent ₹{month:.2f} of ₹{budget:.2f} (₹{remaining:.2f} left)",
                    text_color="#22c55e"
                )
                self.budget_progress.configure(progress_color="#22c55e")
        else:
            self.budget_status_lbl.configure(
                text="Monthly Budget: Not Set",
                text_color=self.text_secondary
            )
            self.budget_progress.set(0)

    # --------------------------------------------------
    # Rendering & Filtering
    # --------------------------------------------------
    def load_expenses(self, expenses=None):
        for widget in self.expenses_scroll.winfo_children():
            widget.destroy()

        if expenses is None:
            filter_mode = self.date_filter_menu.get() if hasattr(self, "date_filter_menu") else "All"
            expenses = self.app.db.get_filtered_expenses(self.user[0], filter_mode)

        # Header Row
        headers_frame = ctk.CTkFrame(self.expenses_scroll, fg_color=self.card_bg, corner_radius=8, height=35)
        headers_frame.pack(fill="x", pady=(0, 6))
        headers_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        ctk.CTkLabel(headers_frame, text="Date", font=("Arial", 12, "bold"), text_color=self.text_secondary).grid(row=0, column=0, pady=6)
        ctk.CTkLabel(headers_frame, text="Category", font=("Arial", 12, "bold"), text_color=self.text_secondary).grid(row=0, column=1, pady=6)
        ctk.CTkLabel(headers_frame, text="Payment", font=("Arial", 12, "bold"), text_color=self.text_secondary).grid(row=0, column=2, pady=6)
        ctk.CTkLabel(headers_frame, text="Amount", font=("Arial", 12, "bold"), text_color=self.text_secondary).grid(row=0, column=3, pady=6)
        ctk.CTkLabel(headers_frame, text="Actions", font=("Arial", 12, "bold"), text_color=self.text_secondary).grid(row=0, column=4, pady=6)

        if not expenses:
            ctk.CTkLabel(self.expenses_scroll, text="No expenses found.", text_color=self.text_secondary).pack(pady=30)
            return

        for exp in expenses:
            exp_id = exp[0]
            amount = exp[1]
            category = exp[2]
            desc = exp[3]
            date = exp[4]
            payment = exp[5] if len(exp) > 5 else "UPI"

            row = ctk.CTkFrame(self.expenses_scroll, fg_color=self.card_bg, corner_radius=10)
            row.pack(fill="x", pady=3)
            row.columnconfigure((0, 1, 2, 3, 4), weight=1)

            ctk.CTkLabel(row, text=str(date), font=("Arial", 12), text_color=self.text_primary).grid(row=0, column=0, padx=5, pady=8)
            ctk.CTkLabel(row, text=str(category), font=("Arial", 12), text_color=self.text_primary).grid(row=0, column=1, padx=5, pady=8)

            pm_badge = ctk.CTkFrame(row, fg_color=self.card_border, corner_radius=6)
            pm_badge.grid(row=0, column=2, padx=5, pady=8)
            ctk.CTkLabel(pm_badge, text=f" {payment} ", font=("Arial", 11, "bold"), text_color="#0284c7").pack(padx=6, pady=2)

            ctk.CTkLabel(row, text=f"₹{amount:.2f}", font=("Arial", 13, "bold"), text_color="#16a34a").grid(row=0, column=3, padx=5, pady=8)

            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.grid(row=0, column=4, padx=5, pady=8)

            edit_btn = ctk.CTkButton(
                actions_frame,
                text="✏️",
                width=34,
                height=26,
                corner_radius=6,
                fg_color="#3b82f6",
                hover_color="#2563eb",
                command=lambda e_id=exp_id: self.edit_expense(e_id)
            )
            edit_btn.pack(side="left", padx=2)

            del_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️",
                width=34,
                height=26,
                corner_radius=6,
                fg_color="#ef4444",
                hover_color="#dc2626",
                command=lambda e_id=exp_id: self.delete_expense(e_id)
            )
            del_btn.pack(side="left", padx=2)

    def on_filter_change(self, choice):
        self.load_expenses()

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
        modal.geometry("380x480")
        modal.grab_set()

        ctk.CTkLabel(modal, text="Add Expense", font=("Arial", 18, "bold")).pack(pady=12)

        amount_entry = ctk.CTkEntry(modal, placeholder_text="Amount (₹)", width=280, height=36)
        amount_entry.pack(pady=6)

        category_entry = ctk.CTkEntry(modal, placeholder_text="Category (e.g. Food, Travel)", width=280, height=36)
        category_entry.pack(pady=6)

        desc_entry = ctk.CTkEntry(modal, placeholder_text="Description (Optional)", width=280, height=36)
        desc_entry.pack(pady=6)

        today_str = datetime.now().strftime("%d-%m-%Y")
        date_entry = ctk.CTkEntry(modal, width=280, height=36)
        date_entry.insert(0, today_str)
        date_entry.pack(pady=6)

        pm_dropdown = ctk.CTkOptionMenu(
            modal,
            values=["UPI", "Cash", "Credit Card", "Debit Card", "Bank Transfer"],
            width=280,
            height=36
        )
        pm_dropdown.pack(pady=6)

        def save():
            try:
                amt = float(amount_entry.get().strip())
                cat = category_entry.get().strip()
                desc = desc_entry.get().strip()
                dt = date_entry.get().strip()
                pm = pm_dropdown.get()

                if not amt or not cat or not dt:
                    messagebox.showerror("Error", "Amount, Category, and Date are required!")
                    return

                datetime.strptime(dt, "%d-%m-%Y")

                self.check_over_budget_alerts(amt, cat)
                self.app.db.add_expense(self.user[0], amt, cat, desc, dt, pm)
                modal.destroy()
                self.update_metrics()
                self.load_expenses()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount or date format (DD-MM-YYYY)!")

        ctk.CTkButton(modal, text="Save Expense", height=38, fg_color="#2563eb", command=save).pack(pady=15)

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
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

    def logout(self):
        from login import LoginPage
        self.frame.destroy()
        LoginPage(self.app)