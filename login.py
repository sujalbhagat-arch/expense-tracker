import customtkinter as ctk
from tkinter import messagebox


class LoginPage(ctk.CTkFrame):

    def __init__(self, app):
        super().__init__(app, fg_color="transparent")
        self.app = app

        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Center Container Card
        self.container = ctk.CTkFrame(self, fg_color="#212529", corner_radius=20)
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.85)

        # Configure 2-Column Grid inside Container
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT PANEL: BRANDING & FEATURES
        # ==========================================
        self.left_frame = ctk.CTkFrame(
            self.container,
            fg_color=("#1f2937", "#1e293b"),
            corner_radius=16
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # App Logo & Title
        ctk.CTkLabel(
            self.left_frame,
            text="💰 Smart Expense Tracker",
            font=("Arial", 22, "bold"),
            text_color="#60a5fa"
        ).pack(anchor="w", padx=25, pady=(35, 5))

        ctk.CTkLabel(
            self.left_frame,
            text="Take control of your personal finances effortlessly.",
            font=("Arial", 12),
            text_color="#94a3b8"
        ).pack(anchor="w", padx=25, pady=(0, 25))

        # Feature Highlights
        features = [
            ("📊 Visual Analytics", "Interactive pie charts & monthly trends."),
            ("🎯 Budget Tracking", "Set category limits & stay notified."),
            ("💳 Payment Modes", "Track UPI, Cash, Cards & Transfers easily.")
        ]

        for title, desc in features:
            f_box = ctk.CTkFrame(self.left_frame, fg_color="transparent")
            f_box.pack(fill="x", padx=25, pady=8)

            ctk.CTkLabel(
                f_box,
                text=title,
                font=("Arial", 14, "bold"),
                text_color="#e2e8f0"
            ).pack(anchor="w")

            ctk.CTkLabel(
                f_box,
                text=desc,
                font=("Arial", 11),
                text_color="#64748b"
            ).pack(anchor="w")

        # ==========================================
        # RIGHT PANEL: LOGIN FORM
        # ==========================================
        self.right_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        # Form Header
        ctk.CTkLabel(
            self.right_frame,
            text="Welcome Back!",
            font=("Arial", 24, "bold"),
            text_color="#ffffff"
        ).pack(anchor="w", pady=(20, 5))

        ctk.CTkLabel(
            self.right_frame,
            text="Please sign in to continue to your dashboard.",
            font=("Arial", 12),
            text_color="#94a3b8"
        ).pack(anchor="w", pady=(0, 25))

        # Username Input
        ctk.CTkLabel(
            self.right_frame,
            text="Username",
            font=("Arial", 12, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(
            self.right_frame,
            placeholder_text="Enter your username",
            height=42,
            border_width=1,
            corner_radius=10,
            font=("Arial", 13)
        )
        self.username_entry.pack(fill="x", pady=(0, 15))

        # Password Input
        ctk.CTkLabel(
            self.right_frame,
            text="Password",
            font=("Arial", 12, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="w", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(
            self.right_frame,
            placeholder_text="Enter your password",
            show="•",
            height=42,
            border_width=1,
            corner_radius=10,
            font=("Arial", 13)
        )
        self.password_entry.pack(fill="x", pady=(0, 25))

        # Login Button
        self.login_btn = ctk.CTkButton(
            self.right_frame,
            text="Sign In 🚀",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.login_action
        )
        self.login_btn.pack(fill="x", pady=(0, 15))

        # Register Link
        self.register_link = ctk.CTkButton(
            self.right_frame,
            text="Don't have an account? Register here",
            font=("Arial", 12, "underline"),
            fg_color="transparent",
            text_color="#38bdf8",
            hover_color=("#1e293b", "#334155"),
            anchor="center",
            command=lambda: self.app.show_register() if hasattr(self.app, "show_register") else self.open_register_fallback()
        )
        self.register_link.pack(fill="x")

    def open_register_fallback(self):
        from register import RegisterPage
        self.destroy()
        RegisterPage(self.app)

    def login_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        user = self.app.db.login_user(username, password)
        if user:
            from dashboard import Dashboard
            self.destroy()
            Dashboard(self.app, user)
        else:
            messagebox.showerror("Error", "Invalid username or password.")