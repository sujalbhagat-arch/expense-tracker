import customtkinter as ctk
from register import RegisterPage
from dashboard import Dashboard

print(">>> LOGIN.PY IS LOADED <<<")


class LoginPage:

    def __init__(self, app):
        self.app = app

        # ------------------------
        # Login Card
        # ------------------------
        self.frame = ctk.CTkFrame(
            master=app,
            width=450,
            height=520,
            corner_radius=20
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # ------------------------
        # Title
        # ------------------------
        self.title = ctk.CTkLabel(
            self.frame,
            text="Smart Expense Tracker",
            font=("Arial", 30, "bold")
        )
        self.title.pack(pady=(30, 10))

        # ------------------------
        # Subtitle
        # ------------------------
        self.subtitle = ctk.CTkLabel(
            self.frame,
            text="Welcome Back!",
            font=("Arial", 16)
        )
        self.subtitle.pack(pady=(0, 25))

        # ------------------------
        # Username
        # ------------------------
        self.username = ctk.CTkEntry(
            self.frame,
            width=320,
            height=40,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        # ------------------------
        # Password
        # ------------------------
        self.password = ctk.CTkEntry(
            self.frame,
            width=320,
            height=40,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        # ------------------------
        # Show Password
        # ------------------------
        self.show_password = ctk.CTkCheckBox(
            self.frame,
            text="Show Password",
            command=self.toggle_password
        )
        self.show_password.pack(anchor="w", padx=60, pady=(5, 20))

        # ------------------------
        # Login Button
        # ------------------------
        self.login_btn = ctk.CTkButton(
            self.frame,
            text="Login",
            width=320,
            height=40,
            command=self.login
        )
        self.login_btn.pack(pady=10)

        # ------------------------
        # Message Label
        # ------------------------
        self.message = ctk.CTkLabel(
            self.frame,
            text="",
            font=("Arial", 14),
            text_color="red"
        )
        self.message.pack(pady=(5, 10))

        # ------------------------
        # Register Button
        # ------------------------
        self.register_btn = ctk.CTkButton(
            self.frame,
            text="Register",
            width=320,
            height=40,
            fg_color="gray",
            hover_color="#5c5c5c",
            command=self.register
        )
        self.register_btn.pack()

    # ------------------------
    # Login Function
    # ------------------------
    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        # Clear old message
        self.message.configure(text="")

        # Check empty fields
        if not username or not password:
            self.message.configure(
                text="Please enter username and password.",
                text_color="red"
            )
            return

        # Check database
        user = self.app.db.check_login(username, password)

        if user:

            self.message.configure(
                text="Login Successful!",
                text_color="green"
            )

            print("✅ Login Successful!")
            print("Welcome,", user[1])

            self.frame.destroy()
            Dashboard(self.app, user)

        else:

            self.message.configure(
                text="Invalid Username or Password",
                text_color="red"
            )

    # ------------------------
    # Register Function
    # ------------------------
    def register(self):
        self.frame.destroy()
        RegisterPage(self.app)

    # ------------------------
    # Show / Hide Password
    # ------------------------
    def toggle_password(self):

        if self.show_password.get() == 1:
            self.password.configure(show="")
        else:
            self.password.configure(show="*")