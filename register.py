import customtkinter as ctk
from tkinter import messagebox


class RegisterPage:

    def __init__(self, parent):
        self.app = parent

        # Register Frame Container
        self.frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both")

        # Main Box Container
        main_box = ctk.CTkFrame(self.frame, corner_radius=15, width=420, height=580)
        main_box.pack(expand=True)
        main_box.pack_propagate(False)

        # Title
        ctk.CTkLabel(
            main_box, 
            text="Create Account 🚀", 
            font=("Arial", 22, "bold")
        ).pack(anchor="w", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            main_box, 
            text="Join Smart Expense Tracker today", 
            font=("Arial", 11), 
            text_color="gray"
        ).pack(anchor="w", padx=30, pady=(0, 15))

        # Full Name Input
        self.name_entry = ctk.CTkEntry(main_box, placeholder_text="Full Name", height=40)
        self.name_entry.pack(fill="x", padx=30, pady=8)

        # Username Input
        self.username_entry = ctk.CTkEntry(main_box, placeholder_text="Username", height=40)
        self.username_entry.pack(fill="x", padx=30, pady=8)

        # Password Input
        self.password_entry = ctk.CTkEntry(main_box, placeholder_text="Password", show="*", height=40)
        self.password_entry.pack(fill="x", padx=30, pady=8)

        # Confirm Password Input
        self.confirm_password_entry = ctk.CTkEntry(main_box, placeholder_text="Confirm Password", show="*", height=40)
        self.confirm_password_entry.pack(fill="x", padx=30, pady=8)

        # Register Button
        ctk.CTkButton(
            main_box, 
            text="Register 👤", 
            height=40, 
            font=("Arial", 13, "bold"), 
            command=self.handle_register
        ).pack(fill="x", padx=30, pady=(20, 15))

        # Back to Login Link
        login_link = ctk.CTkButton(
            main_box, 
            text="Already have an account? Sign In", 
            fg_color="transparent", 
            hover=False, 
            text_color="#3b82f6", 
            command=self.open_login
        )
        login_link.pack()

    def handle_register(self):
        full_name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_pass = self.confirm_password_entry.get().strip()

        if not full_name or not username or not password:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        if password != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Pass full_name as well so database handles it safely
        success = self.app.db.add_user(username, password, full_name)

        if success:
            messagebox.showinfo("Success", "Account created successfully! Please Sign In.")
            self.open_login()
        else:
            messagebox.showerror("Error", "Username already exists. Please pick another.")

    def open_login(self):
        from login import LoginPage
        self.frame.destroy()
        LoginPage(self.app)