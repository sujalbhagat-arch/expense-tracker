import customtkinter as ctk
from login import LoginPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Expense Tracker")
app.geometry("1000x600")
app.minsize(900, 550)

LoginPage(app)

app.mainloop()