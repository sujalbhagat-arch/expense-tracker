import customtkinter as ctk


class EditExpensePage:

    def __init__(self, app, expense_id):

        self.app = app
        self.expense_id = expense_id

        # Get expense from database
        expense = self.app.db.get_expense(expense_id)

        self.window = ctk.CTkToplevel(app)
        self.window.title("Edit Expense")
        self.window.geometry("400x420")
        self.window.grab_set()

        # Amount
        ctk.CTkLabel(self.window, text="Amount").pack(pady=(20, 5))
        self.amount = ctk.CTkEntry(self.window, width=250)
        self.amount.pack()
        self.amount.insert(0, str(expense[0]))

        # Category
        ctk.CTkLabel(self.window, text="Category").pack(pady=(15, 5))
        self.category = ctk.CTkEntry(self.window, width=250)
        self.category.pack()
        self.category.insert(0, expense[1])

        # Description
        ctk.CTkLabel(self.window, text="Description").pack(pady=(15, 5))
        self.description = ctk.CTkEntry(self.window, width=250)
        self.description.pack()
        self.description.insert(0, expense[2])

        # Date
        ctk.CTkLabel(self.window, text="Date (DD-MM-YYYY)").pack(pady=(15, 5))
        self.date = ctk.CTkEntry(self.window, width=250)
        self.date.pack()
        self.date.insert(0, expense[3])

        # Update Button
        ctk.CTkButton(
            self.window,
            text="Update Expense",
            command=self.update_expense
        ).pack(pady=30)

    def update_expense(self):

        amount = float(self.amount.get())
        category = self.category.get()
        description = self.description.get()
        expense_date = self.date.get()

        self.app.db.update_expense(
            self.expense_id,
            amount,
            category,
            description,
            expense_date
        )

        print("✅ Expense Updated")

        self.window.destroy()