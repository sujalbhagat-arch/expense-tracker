import customtkinter as ctk
from login import LoginPage
from database import Database

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create Database
db = Database()

# Create Main Window
app = ctk.CTk()
app.title("Smart Expense Tracker")
app.geometry("1000x600")
app.minsize(900, 550)

# Attach database to app
app.db = db

# Open Login Page
LoginPage(app)

# Run Application
app.mainloop()