import customtkinter as ctk
from login import LoginPage

# App Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create Window
app = ctk.CTk()

app.title("Smart Expense Tracker")
app.geometry("1000x600")
app.minsize(900, 550)

# Load Login Page
LoginPage(app)

# Run App
app.mainloop()