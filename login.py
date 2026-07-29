import customtkinter as ctk


class LoginPage:

    def __init__(self, app):
        self.app = app

        # Login Card
        self.frame = ctk.CTkFrame(
            master=app,
            width=450,
            height=480,
            corner_radius=20
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        self.title = ctk.CTkLabel(
            self.frame,
            text="Smart Expense Tracker",
            font=("Arial", 30, "bold")
        )
        self.title.pack(pady=(30, 10))

        # Subtitle
        self.subtitle = ctk.CTkLabel(
            self.frame,
            text="Welcome Back!",
            font=("Arial", 16)
        )
        self.subtitle.pack(pady=(0, 25))

        # Username Entry
        self.username = ctk.CTkEntry(
            self.frame,
            width=320,
            height=40,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        # Password Entry
        self.password = ctk.CTkEntry(
            self.frame,
            width=320,
            height=40,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        # Show Password Checkbox
        self.show_password = ctk.CTkCheckBox(
            self.frame,
            text="Show Password",
            command=self.toggle_password
        )
        self.show_password.pack(anchor="w", padx=60, pady=(5, 20))

        # Login Button
        self.login_btn = ctk.CTkButton(
            self.frame,
            text="Login",
            width=320,
            height=40,
            command=self.login
        )
        self.login_btn.pack(pady=10)

        # Register Button
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
        username = self.username.get()
        password = self.password.get()

        print("Username:", username)
        print("Password:", password)

    # ------------------------
    # Register Button
    # ------------------------
    def register(self):
        print("Register Button Clicked")

    # ------------------------
    # Show / Hide Password
    # ------------------------
    def toggle_password(self):

        if self.show_password.get() == 1:
            self.password.configure(show="")
        else:
            self.password.configure(show="*")