import tkinter as tk
from tkinter import ttk

class ClientDashboard:
    def __init__(self, master, data_manager, username, user_data, logout_callback, show_account_details_callback):
        self.master = master
        self.data_manager = data_manager
        self.username = username
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.show_account_details_callback = show_account_details_callback
        self.frame = None
    
    def show(self):
        # Clear previous content
        if self.frame:
            self.frame.destroy()
        
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        welcome_label = ttk.Label(
            header_frame,
            text=f"Welcome, {self.user_data['name']}"
        )
        welcome_label.pack(side=tk.LEFT)

        logout_button = ttk.Button(header_frame, text="Logout", command=self.logout_callback)
        logout_button.pack(side=tk.RIGHT)

        # Main content frame
        content_frame = ttk.Frame(self.frame, padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Your Accounts section
        ttk.Label(content_frame, text="Your Accounts", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        # Get user accounts
        user_accounts = self.data_manager.get_user_accounts(self.username)

        if user_accounts:
            for account_id, account in user_accounts.items():
                # Create account card
                account_frame = ttk.Frame(content_frame, padding=10)
                account_frame.pack(fill=tk.X, pady=5)

                # Account info
                ttk.Label(account_frame, text=f"Account: {account_id}", font=('Arial', 12, 'bold')).grid(row=0,
                                                                                                  column=0,
                                                                                                  sticky="w")
                ttk.Label(account_frame, text=f"Type: {account['type'].capitalize()}").grid(row=1, column=0, sticky="w")
                ttk.Label(account_frame, text=f"Balance: ${account['balance']:.2f}", font=('Arial', 12, 'bold')).grid(
                    row=0, column=1, sticky="e")
                ttk.Label(account_frame, text=f"Created: {account['created_at']}").grid(row=1, column=1, sticky="e")

                # View details button
                details_button = ttk.Button(
                    account_frame,
                    text="Manage Account",
                    command=lambda acc_id=account_id: self.show_account_details_callback(acc_id)
                )
                details_button.grid(row=2, column=0, columnspan=2, pady=10)

                # Add separator
                ttk.Separator(content_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        else:
            ttk.Label(content_frame, text="You don't have any accounts yet.").pack(pady=20)
