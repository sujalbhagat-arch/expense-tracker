import customtkinter as ctk
from dashboard import Dashboard


class LoginPage:

    def __init__(self, app):
        self.app = app

        # Main Container Frame
        self.frame = ctk.CTkFrame(master=app, corner_radius=15)
        self.frame.pack(padx=40, pady=40, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.frame,
            text="💰 Smart Expense Tracker",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=(30, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.frame,
            text="Login to manage your expenses",
            font=("Arial", 14),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Username",
            width=280,
            height=40
        )
        self.username_entry.pack(pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Password",
            show="*",
            width=280,
            height=40
        )
        self.password_entry.pack(pady=10)

        # Status / Error Message Label
        self.status_label = ctk.CTkLabel(
            self.frame,
            text="",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=5)

        # Login Button
        self.login_btn = ctk.CTkButton(
            self.frame,
            text="Login",
            width=280,
            height=40,
            command=self.login
        )
        self.login_btn.pack(pady=10)

        # Register Switch Button
        self.register_btn = ctk.CTkButton(
            self.frame,
            text="Don't have an account? Register",
            fg_color="transparent",
            text_color=("#3700b3", "#03dac6"),
            hover=False,
            command=self.show_register
        )
        self.register_btn.pack(pady=5)

    # --------------------------------------------------
    # Login Logic
    # --------------------------------------------------
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.status_label.configure(
                text="Please enter both username and password.",
                text_color="#e74c3c"
            )
            return

        # Connects to Database (using login_user)
        user = self.app.db.login_user(username, password)

        if user:
            print(f"✅ Login Successful! Welcome, {user[1]}")
            self.frame.destroy()
            Dashboard(self.app, user)
        else:
            self.status_label.configure(
                text="Invalid username or password.",
                text_color="#e74c3c"
            )

    # --------------------------------------------------
    # Registration Screen Switch
    # --------------------------------------------------
    def show_register(self):
        self.frame.destroy()
        RegisterPage(self.app)


class RegisterPage:

    def __init__(self, app):
        self.app = app

        # Main Container Frame
        self.frame = ctk.CTkFrame(master=app, corner_radius=15)
        self.frame.pack(padx=40, pady=40, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.frame,
            text="📝 Create Account",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=(30, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.frame,
            text="Sign up to start tracking your expenses",
            font=("Arial", 14),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Choose a Username",
            width=280,
            height=40
        )
        self.username_entry.pack(pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Choose a Password",
            show="*",
            width=280,
            height=40
        )
        self.password_entry.pack(pady=10)

        # Confirm Password Entry
        self.confirm_password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Confirm Password",
            show="*",
            width=280,
            height=40
        )
        self.confirm_password_entry.pack(pady=10)

        # Status / Error Message Label
        self.status_label = ctk.CTkLabel(
            self.frame,
            text="",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=5)

        # Register Button
        self.register_btn = ctk.CTkButton(
            self.frame,
            text="Register Account",
            width=280,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.register
        )
        self.register_btn.pack(pady=10)

        # Back to Login Button
        self.back_btn = ctk.CTkButton(
            self.frame,
            text="Already have an account? Login",
            fg_color="transparent",
            text_color=("#3700b3", "#03dac6"),
            hover=False,
            command=self.show_login
        )
        self.back_btn.pack(pady=5)

    # --------------------------------------------------
    # Registration Logic
    # --------------------------------------------------
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            self.status_label.configure(
                text="Please fill in all fields.",
                text_color="#e74c3c"
            )
            return

        if password != confirm_password:
            self.status_label.configure(
                text="Passwords do not match!",
                text_color="#e74c3c"
            )
            return

        # Attempt to insert into database
        success = self.app.db.register_user(username, password)

        if success:
            self.status_label.configure(
                text="Account created! You can now log in.",
                text_color="#2ecc71"
            )
            self.frame.after(1500, self.show_login)
        else:
            self.status_label.configure(
                text="Username already exists. Choose another.",
                text_color="#e74c3c"
            )

    # --------------------------------------------------
    # Login Screen Switch
    # --------------------------------------------------
    def show_login(self):
        self.frame.destroy()
        LoginPage(self.app)