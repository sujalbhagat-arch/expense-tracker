import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class ExpensePage:

    def __init__(self, app, user):

        self.app = app
        self.user = user

        # ------------------------
        # Popup Window
        # ------------------------
        self.window = ctk.CTkToplevel(app)
        self.window.title("Add Expense")
        self.window.geometry("450x500")
        self.window.resizable(False, False)

        # Make popup stay on top
        self.window.grab_set()

        # ------------------------
        # Title
        # ------------------------
        title = ctk.CTkLabel(
            self.window,
            text="Add Expense",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        # ------------------------
        # Amount
        # ------------------------
        self.amount = ctk.CTkEntry(
            self.window,
            width=300,
            height=40,
            placeholder_text="Amount (₹)"
        )
        self.amount.pack(pady=10)

        # ------------------------
        # Category
        # ------------------------
        self.category = ctk.CTkComboBox(
            self.window,
            width=300,
            height=40,
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Health",
                "Education",
                "Other"
            ]
        )
        self.category.set("Food")
        self.category.pack(pady=10)

        # ------------------------
        # Description
        # ------------------------
        self.description = ctk.CTkEntry(
            self.window,
            width=300,
            height=40,
            placeholder_text="Description"
        )
        self.description.pack(pady=10)

        # ------------------------
        # Date
        # ------------------------
        self.date = ctk.CTkEntry(
            self.window,
            width=300,
            height=40
        )
        self.date.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.date.pack(pady=10)

        # ------------------------
        # Save Button
        # ------------------------
        save_btn = ctk.CTkButton(
            self.window,
            text="Save Expense",
            width=300,
            height=40,
            command=self.save_expense
        )
        save_btn.pack(pady=25)

    # ------------------------
    # Save Expense
    # ------------------------
    def save_expense(self):

        amount = self.amount.get().strip()
        category = self.category.get()
        description = self.description.get().strip()
        expense_date = self.date.get().strip()

        # Validation
        if amount == "":
            messagebox.showerror("Error", "Please enter amount.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        # Save to database
        self.app.db.add_expense(
            self.user[0],      # user_id
            amount,
            category,
            description,
            expense_date
        )

        messagebox.showinfo("Success", "Expense Added Successfully!")

        self.window.destroy()