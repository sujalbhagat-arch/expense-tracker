import customtkinter as ctk


class RegisterPage:

    def __init__(self, app):

        self.app = app

        self.frame = ctk.CTkFrame(
            master=app,
            width=450,
            height=550,
            corner_radius=20
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            self.frame,
            text="Create New Account",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(30, 20))

        self.name = ctk.CTkEntry(
            self.frame,
            width=320,
            placeholder_text="Full Name"
        )
        self.name.pack(pady=10)

        self.username = ctk.CTkEntry(
            self.frame,
            width=320,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            self.frame,
            width=320,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        self.confirm = ctk.CTkEntry(
            self.frame,
            width=320,
            placeholder_text="Confirm Password",
            show="*"
        )
        self.confirm.pack(pady=10)

        self.register_btn = ctk.CTkButton(
            self.frame,
            text="Create Account",
            width=320,
            height=40
        )
        self.register_btn.pack(pady=20)