import customtkinter as ctk
from database import Database
from login import LoginPage


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Smart Expense Tracker")
        self.geometry("900x600")
        ctk.set_appearance_mode("Dark")

        # Single shared database instance
        self.db = Database("expense_tracker.db")

        # Window Close Handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load Login Page
        LoginPage(self)

    def on_closing(self):
        try:
            self.withdraw()
            self.quit()
            self.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()