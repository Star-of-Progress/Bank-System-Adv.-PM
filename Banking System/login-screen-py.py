import tkinter as tk
from tkinter import ttk, messagebox

class LoginScreen:
    def __init__(self, master, login_callback):
        self.master = master
        self.login_callback = login_callback
        self.frame = None
    
    def show(self):
        # Clear previous content
        if self.frame:
            self.frame.destroy()
        
        # Login form
        self.frame = ttk.Frame(self.master, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(self.frame, text="Banking System Login", style="Header.TLabel").pack(pady=20)

        # Username
        ttk.Label(self.frame, text="Username:").pack(pady=(10, 5), anchor="w")
        self.username_entry = ttk.Entry(self.frame, width=30)
        self.username_entry.pack(pady=(0, 10), fill="x")

        # Password
        ttk.Label(self.frame, text="Password:").pack(pady=(10, 5), anchor="w")
        self.password_entry = ttk.Entry(self.frame, width=30, show="*")
        self.password_entry.pack(pady=(0, 10), fill="x")

        # Login button
        login_button = ttk.Button(
            self.frame,
            text="Login",
            command=self.attempt_login
        )
        login_button.pack(pady=20)

        # Set focus on username entry
        self.username_entry.focus()
    
    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password")
            return
        
        self.login_callback(username, password)
