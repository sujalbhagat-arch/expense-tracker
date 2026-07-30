import customtkinter as ctk
from database import Database
from login import LoginPage


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Smart Expense Tracker")
        self.geometry("900x650")

        # Initialize Database
        self.db = Database()

        # Handle window close protocol gracefully to prevent background bgerrors
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load Login Page
        LoginPage(self)

    def on_closing(self):
        """Safely destroy the window and stop background CustomTkinter loops."""
        try:
            self.withdraw()  # Hide window first to prevent rendering updates
            self.quit()      # Stop Tcl mainloop
            self.destroy()   # Destroy widgets cleanly
        except Exception:
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()