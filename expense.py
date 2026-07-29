import customtkinter as ctk

# -----------------------------
# Application Settings
# -----------------------------
ctk.set_appearance_mode("dark")      # Modes: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blu


# -----------------------------
# Create Main Window
# -----------------------------
app = ctk.CTk()

app.title("Smart Expense Tracker")
app.geometry("1000x600")
app.minsize(900, 550)

# -----------------------------
# Welcome Label
# ----------------------------
title = ctk.CTkLabel(app, text="Smart Expense Tracker", font=("Arial", 30, "bold"))
title.pack(pady=30)
subtitle = ctk.CTkLabel(
app,
    text="Developed using Python & CustomTkinter",
    font=("Arial", 16)
)

subtitle.pack()     
# -----------------------------
# Start Application
# -----------------------------
app.mainloop()