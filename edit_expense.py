import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class EditExpensePage:

    def __init__(self, app, expense_id):
        self.app = app
        self.expense_id = expense_id

        # Fetch expense data: (id, amount, category, description, date, payment_method)
        self.expense = self.app.db.get_expense(expense_id)

        if not self.expense:
            messagebox.showerror("Error", "Expense not found!")
            return

        # Popup Window Setup
        self.window = ctk.CTkToplevel(app)
        self.window.title("Edit Expense")
        self.window.geometry("400x520")
        self.window.grab_set()

        ctk.CTkLabel(self.window, text="Edit Expense", font=("Arial", 20, "bold")).pack(pady=15)

        # Amount Entry
        ctk.CTkLabel(self.window, text="Amount (₹)").pack(anchor="w", padx=50)
        self.amount_entry = ctk.CTkEntry(self.window, width=300)
        self.amount_entry.pack(pady=(0, 10))

        # Category Entry
        ctk.CTkLabel(self.window, text="Category").pack(anchor="w", padx=50)
        self.category_entry = ctk.CTkEntry(self.window, width=300)
        self.category_entry.pack(pady=(0, 10))

        # Description Entry
        ctk.CTkLabel(self.window, text="Description").pack(anchor="w", padx=50)
        self.desc_entry = ctk.CTkEntry(self.window, width=300)
        self.desc_entry.pack(pady=(0, 10))

        # Date Entry
        ctk.CTkLabel(self.window, text="Date (DD-MM-YYYY)").pack(anchor="w", padx=50)
        self.date_entry = ctk.CTkEntry(self.window, width=300)
        self.date_entry.pack(pady=(0, 10))

        # Payment Method Dropdown
        ctk.CTkLabel(self.window, text="Payment Method").pack(anchor="w", padx=50)
        self.payment_dropdown = ctk.CTkOptionMenu(
            self.window,
            values=["UPI", "Cash", "Credit Card", "Debit Card", "Bank Transfer"],
            width=300
        )
        self.payment_dropdown.pack(pady=(0, 15))

        # Populate fields with existing data safely
        self.amount_entry.insert(0, str(self.expense[1]))
        self.category_entry.insert(0, str(self.expense[2]))

        if self.expense[3]:
            self.desc_entry.insert(0, str(self.expense[3]))

        self.date_entry.insert(0, str(self.expense[4]))

        # Handle payment method field safely if present
        current_pm = self.expense[5] if len(self.expense) > 5 and self.expense[5] else "UPI"
        self.payment_dropdown.set(current_pm)

        # Update Button
        self.update_btn = ctk.CTkButton(
            self.window,
            text="Update Expense",
            command=self.update_expense_action
        )
        self.update_btn.pack(pady=10)

    def update_expense_action(self):
        try:
            amount_str = self.amount_entry.get().strip()
            category = self.category_entry.get().strip()
            description = self.desc_entry.get().strip()
            date = self.date_entry.get().strip()
            payment_method = self.payment_dropdown.get()

            if not amount_str or not category or not date:
                messagebox.showerror("Error", "Amount, Category, and Date are required!")
                return

            amount = float(amount_str)

            # Validate date format (DD-MM-YYYY)
            datetime.strptime(date, "%d-%m-%Y")

            # Update database record
            self.app.db.update_expense(
                self.expense_id,
                amount,
                category,
                description,
                date,
                payment_method
            )

            messagebox.showinfo("Success", "Expense updated successfully!")
            self.window.destroy()

            # Safely refresh the dashboard metrics and list
            if hasattr(self.app, "current_dashboard") and self.app.current_dashboard:
                self.app.current_dashboard.update_metrics()
                self.app.current_dashboard.load_expenses()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount or date format! Use DD-MM-YYYY.")