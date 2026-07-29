import customtkinter as ctk


class RegisterPage:

    def __init__(self, app):
        self.app = app

        # ------------------------
        # Register Card
        # ------------------------
        self.frame = ctk.CTkFrame(
            master=app,
            width=450,
            height=550,
            corner_radius=20
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # ------------------------
        # Title
        # ------------------------
        self.title = ctk.CTkLabel(
            self.frame,
            text="Create New Account",
            font=("Arial", 28, "bold")
        )
        self.title.pack(pady=(30, 20))

        # ------------------------
        # Full Name
        # ------------------------
        self.name = ctk.CTkEntry(
            self.frame,
            width=320,
            height=40,
            placeholder_text="Full Name"
        )
        self.name.pack(pady=10)

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
        # Confirm Password
        # ------------------------
        self.confirm = ctk.CTkEntry(
            self.frame,
            width=320,
            height=40,
            placeholder_text="Confirm Password",
            show="*"
        )
        self.confirm.pack(pady=10)

        # ------------------------
        # Create Account Button
        # ------------------------
        self.register_btn = ctk.CTkButton(
            self.frame,
            text="Create Account",
            width=320,
            height=40,
            command=self.create_account
        )
        self.register_btn.pack(pady=20)

    # ------------------------
    # Create Account Function
    # ------------------------
    def create_account(self):

        # Get user input
        name = self.name.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm.get()

        # Check if any field is empty
        if not name or not username or not password or not confirm:
            print("Please fill all fields.")
            return

        # Check if passwords match
        if password != confirm:
            print("Passwords do not match.")
            return

        # Save user to database
        try:
            self.app.db.add_user(name, username, password)
            print("User Saved Successfully!")

        except Exception as e:
            print("Error:", e)
        