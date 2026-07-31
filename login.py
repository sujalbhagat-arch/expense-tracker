import customtkinter as ctk
from tkinter import messagebox
from dashboard import Dashboard


class LoginPage:

    def __init__(self, parent):
        self.app = parent

        # Login Frame Container
        self.frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both")

        # Split Layout Container
        main_box = ctk.CTkFrame(self.frame, corner_radius=15, width=700, height=450)
        main_box.pack(expand=True)
        main_box.pack_propagate(False)

        # Left Banner Panel
        left_panel = ctk.CTkFrame(main_box, fg_color="#1e293b", corner_radius=15, width=320)
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            left_panel, 
            text="💰 Smart Expense Tracker", 
            font=("Arial", 18, "bold"), 
            text_color="#60a5fa"
        ).pack(anchor="w", padx=20, pady=(30, 5))

        ctk.CTkLabel(
            left_panel, 
            text="Take control of your personal finances effortlessly.", 
            font=("Arial", 11), 
            text_color="#94a3b8", 
            wraplength=260, 
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 20))

        # Features List
        features = [
            ("📊 Visual Analytics", "Interactive pie charts & monthly trends."),
            ("🎯 Budget Tracking", "Set category limits & stay notified."),
            ("💳 Payment Modes", "Track UPI, Cash, Cards & Transfers easily.")
        ]
        for title, desc in features:
            f_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
            f_frame.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(f_frame, text=title, font=("Arial", 12, "bold"), text_color="#f8fafc").pack(anchor="w")
            ctk.CTkLabel(f_frame, text=desc, font=("Arial", 10), text_color="#64748b").pack(anchor="w")

        # Right Login Form Panel
        right_panel = ctk.CTkFrame(main_box, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(right_panel, text="Welcome Back!", font=("Arial", 22, "bold")).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(right_panel, text="Please sign in to continue to your dashboard", font=("Arial", 11), text_color="gray").pack(anchor="w", pady=(0, 20))

        # Username Input
        self.username_entry = ctk.CTkEntry(right_panel, placeholder_text="Username", height=40)
        self.username_entry.pack(fill="x", pady=10)

        # Password Input
        self.password_entry = ctk.CTkEntry(right_panel, placeholder_text="Password", show="*", height=40)
        self.password_entry.pack(fill="x", pady=10)

        # Sign In Button
        ctk.CTkButton(
            right_panel, 
            text="Sign In 🚀", 
            height=40, 
            font=("Arial", 13, "bold"), 
            command=self.handle_login
        ).pack(fill="x", pady=15)

        # Register Switch Link
        register_link = ctk.CTkButton(
            right_panel, 
            text="Don't have an account? Register here", 
            fg_color="transparent", 
            hover=False, 
            text_color="#3b82f6", 
            command=self.open_register
        )
        register_link.pack()

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password!")
            return

        # Query Database
        user = self.app.db.login_user(username, password)

        # Fallback check (case-insensitive username)
        if not user:
            self.app.db.cursor.execute(
                "SELECT id, username FROM users WHERE LOWER(username) = LOWER(?) AND password = ?", 
                (username, password)
            )
            user = self.app.db.cursor.fetchone()

        if user:
            self.frame.destroy()
            Dashboard(self.app, user)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        from register import RegisterPage
        self.frame.destroy()
        RegisterPage(self.app)