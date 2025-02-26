import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import hashlib
import datetime


class BankSystem:
    def __init__(self):
        # Data storage file
        self.DATA_FILE = 'bank_data.json'
        self.current_user = None
        self.user_role = None

        # Load data or create default if file doesn't exist
        self.load_data()

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Banking System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Set styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, relief="flat", background="#1e88e5")
        self.style.configure("TLabel", background="#f0f0f0", font=('Arial', 11))
        self.style.configure("Header.TLabel", font=('Arial', 18, 'bold'))

        # Create the main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Show login screen initially
        self.show_login()

    def load_data(self):
        if not os.path.exists(self.DATA_FILE):
            # Create default data with admin user
            default_data = {
                'users': {
                    'admin': {
                        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
                        'role': 'admin',
                        'name': 'System Administrator'
                    }
                },
                'accounts': {}
            }
            with open(self.DATA_FILE, 'w') as f:
                json.dump(default_data, f, indent=4)
            self.data = default_data
        else:
            # Load existing data
            with open(self.DATA_FILE, 'r') as f:
                self.data = json.load(f)

    def save_data(self):
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def clear_frame(self):
        # Destroy all widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_frame()

        # Login form
        login_frame = ttk.Frame(self.main_frame, padding="20")
        login_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(login_frame, text="Banking System Login", style="Header.TLabel").pack(pady=20)

        # Username
        ttk.Label(login_frame, text="Username:").pack(pady=(10, 5), anchor="w")
        username_entry = ttk.Entry(login_frame, width=30)
        username_entry.pack(pady=(0, 10), fill="x")

        # Password
        ttk.Label(login_frame, text="Password:").pack(pady=(10, 5), anchor="w")
        password_entry = ttk.Entry(login_frame, width=30, show="*")
        password_entry.pack(pady=(0, 10), fill="x")

        # Login button
        login_button = ttk.Button(
            login_frame,
            text="Login",
            command=lambda: self.login(username_entry.get(), password_entry.get())
        )
        login_button.pack(pady=20)

        # Set focus on username entry
        username_entry.focus()

    def create_account(self, owner, account_type, initial_balance):
        if not owner:
            messagebox.showerror("Error", "Please select an owner")
            return

        if initial_balance < 0:
            messagebox.showerror("Error", "Initial balance cannot be negative")
            return

        account_id = f"ACC{len(self.data['accounts']) + 1:06d}"

        self.data['accounts'][account_id] = {
            'owner': owner,
            'type': account_type,
            'balance': initial_balance,
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': [
                {
                    'type': 'deposit',
                    'amount': initial_balance,
                    'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'description': 'Initial deposit'
                }
            ]
        }

        self.save_data()
        messagebox.showinfo("Success", f"Account {account_id} created successfully")

        # Refresh the admin dashboard to show the new account
        self.show_admin_dashboard()

    def login(self, username, password):
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password")
            return

        # Check if username exists and password matches
        if (username in self.data['users'] and
                self.data['users'][username]['password'] == hashlib.sha256(password.encode()).hexdigest()):

            self.current_user = username
            self.user_role = self.data['users'][username]['role']

            # Redirect to the appropriate dashboard
            if self.user_role == 'admin':
                self.show_admin_dashboard()
            else:
                self.show_client_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def logout(self):
        self.current_user = None
        self.user_role = None
        self.show_login()

    def show_admin_dashboard(self):
        self.clear_frame()

        # Create a notebook (tab control)
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # User Management Tab
        user_frame = ttk.Frame(notebook, padding=10)
        notebook.add(user_frame, text="User Management")

        # Account Management Tab
        account_frame = ttk.Frame(notebook, padding=10)
        notebook.add(account_frame, text="Account Management")

        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        welcome_label = ttk.Label(
            header_frame,
            text=f"Welcome, {self.data['users'][self.current_user]['name']} (Admin)"
        )
        welcome_label.pack(side=tk.LEFT)

        logout_button = ttk.Button(header_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT)

        # USER MANAGEMENT TAB CONTENT
        # Create new user form
        ttk.Label(user_frame, text="Create New User", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        user_form_frame = ttk.Frame(user_frame)
        user_form_frame.pack(fill=tk.X, pady=10)

        # Username
        ttk.Label(user_form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        username_entry = ttk.Entry(user_form_frame, width=30)
        username_entry.grid(row=0, column=1, sticky="w", pady=5)

        # Password
        ttk.Label(user_form_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        password_entry = ttk.Entry(user_form_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Full Name
        ttk.Label(user_form_frame, text="Full Name:").grid(row=2, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(user_form_frame, width=30)
        name_entry.grid(row=2, column=1, sticky="w", pady=5)

        # Role
        ttk.Label(user_form_frame, text="Role:").grid(row=3, column=0, sticky="w", pady=5)
        role_var = tk.StringVar()
        role_combobox = ttk.Combobox(user_form_frame, textvariable=role_var, state="readonly")
        role_combobox['values'] = ('client', 'admin')
        role_combobox.current(0)
        role_combobox.grid(row=3, column=1, sticky="w", pady=5)

        # Create button
        create_user_button = ttk.Button(
            user_form_frame,
            text="Create User",
            command=lambda: self.create_user(
                username_entry.get(),
                password_entry.get(),
                name_entry.get(),
                role_var.get()
            )
        )
        create_user_button.grid(row=4, column=0, columnspan=2, pady=10)

        # User List
        ttk.Label(user_frame, text="User List", style="Header.TLabel").pack(anchor="w", pady=(20, 10))

        # Create Treeview for user list
        user_tree = ttk.Treeview(user_frame, columns=("username", "name", "role"), show="headings")
        user_tree.pack(fill=tk.BOTH, expand=True)

        # Define headings
        user_tree.heading("username", text="Username")
        user_tree.heading("name", text="Full Name")
        user_tree.heading("role", text="Role")

        # Define column widths
        user_tree.column("username", width=150)
        user_tree.column("name", width=250)
        user_tree.column("role", width=100)

        # Add scrollbar
        user_scroll = ttk.Scrollbar(user_tree, orient="vertical", command=user_tree.yview)
        user_tree.configure(yscrollcommand=user_scroll.set)
        user_scroll.pack(side="right", fill="y")

        # Populate user data
        for username, user_data in self.data['users'].items():
            user_tree.insert("", "end", values=(username, user_data['name'], user_data['role']))

        # ACCOUNT MANAGEMENT TAB CONTENT
        # Create new account form
        ttk.Label(account_frame, text="Create New Account", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        account_form_frame = ttk.Frame(account_frame)
        account_form_frame.pack(fill=tk.X, pady=10)

        # Owner (Client) dropdown
        ttk.Label(account_form_frame, text="Owner (Client):").grid(row=0, column=0, sticky="w", pady=5)
        owner_var = tk.StringVar()
        owner_combobox = ttk.Combobox(account_form_frame, textvariable=owner_var, state="readonly")

        # Populate with client users only
        client_users = [(username, user['name']) for username, user in self.data['users'].items()
                        if user['role'] == 'client']
        owner_combobox['values'] = [f"{name} ({username})" for username, name in client_users]
        if client_users:
            owner_combobox.current(0)
        owner_combobox.grid(row=0, column=1, sticky="w", pady=5)

        # Account Type
        ttk.Label(account_form_frame, text="Account Type:").grid(row=1, column=0, sticky="w", pady=5)
        type_var = tk.StringVar()
        type_combobox = ttk.Combobox(account_form_frame, textvariable=type_var, state="readonly")
        type_combobox['values'] = ('checking', 'savings', 'investment')
        type_combobox.current(0)
        type_combobox.grid(row=1, column=1, sticky="w", pady=5)

        # Initial Balance
        ttk.Label(account_form_frame, text="Initial Balance:").grid(row=2, column=0, sticky="w", pady=5)
        balance_var = tk.DoubleVar(value=0.0)
        balance_entry = ttk.Entry(account_form_frame, textvariable=balance_var, width=30)
        balance_entry.grid(row=2, column=1, sticky="w", pady=5)

        # Create button
        create_account_button = ttk.Button(
            account_form_frame,
            text="Create Account",
            command=lambda: self.create_account(
                owner_var.get().split('(')[1].split(')')[0] if owner_var.get() else "",
                type_var.get(),
                balance_var.get()
            )
        )
        create_account_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Account List
        ttk.Label(account_frame, text="Account List", style="Header.TLabel").pack(anchor="w", pady=(20, 10))

        # Create Treeview for account list
        account_tree = ttk.Treeview(
            account_frame,
            columns=("id", "owner", "type", "balance", "created"),
            show="headings"
        )
        account_tree.pack(fill=tk.BOTH, expand=True)

        # Define headings
        account_tree.heading("id", text="Account ID")
        account_tree.heading("owner", text="Owner")
        account_tree.heading("type", text="Type")
        account_tree.heading("balance", text="Balance")
        account_tree.heading("created", text="Created")

        # Define column widths
        account_tree.column("id", width=100)
        account_tree.column("owner", width=200)
        account_tree.column("type", width=100)
        account_tree.column("balance", width=100)
        account_tree.column("created", width=150)

        # Add scrollbar
        account_scroll = ttk.Scrollbar(account_tree, orient="vertical", command=account_tree.yview)
        account_tree.configure(yscrollcommand=account_scroll.set)
        account_scroll.pack(side="right", fill="y")

        # Add double-click event for account details
        account_tree.bind("<Double-1>",
                          lambda event: self.show_account_details(account_tree.item(account_tree.focus())["values"][0]))

        # Populate account data
        for account_id, account_data in self.data['accounts'].items():
            owner_name = self.data['users'][account_data['owner']]['name']
            account_tree.insert(
                "", "end",
                values=(
                    account_id,
                    f"{owner_name} ({account_data['owner']})",
                    account_data['type'],
                    f"${account_data['balance']:.2f}",
                    account_data['created_at']
                )
            )

    def show_client_dashboard(self):
        self.clear_frame()

        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        welcome_label = ttk.Label(
            header_frame,
            text=f"Welcome, {self.data['users'][self.current_user]['name']}"
        )
        welcome_label.pack(side=tk.LEFT)

        logout_button = ttk.Button(header_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT)

        # Main content frame
        content_frame = ttk.Frame(self.main_frame, padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Your Accounts section
        ttk.Label(content_frame, text="Your Accounts", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        # Get user accounts
        user_accounts = {acc_id: acc for acc_id, acc in self.data['accounts'].items()
                         if acc['owner'] == self.current_user}

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
                    command=lambda acc_id=account_id: self.show_account_details(acc_id)
                )
                details_button.grid(row=2, column=0, columnspan=2, pady=10)

                # Add separator
                ttk.Separator(content_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        else:
            ttk.Label(content_frame, text="You don't have any accounts yet.").pack(pady=20)

    def show_account_details(self, account_id):
        if account_id not in self.data['accounts']:
            messagebox.showerror("Error", "Account does not exist")
            return

        account = self.data['accounts'][account_id]

        # Check if current user is admin or the account owner
        if self.user_role != 'admin' and account['owner'] != self.current_user:
            messagebox.showerror("Error", "You don't have permission to view this account")
            return

        # Create a new window for account details
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Account Details - {account_id}")
        detail_window.geometry("700x500")
        detail_window.transient(self.root)
        detail_window.grab_set()

        # Main frame
        main_frame = ttk.Frame(detail_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Account summary section
        summary_frame = ttk.Frame(main_frame, padding=10)
        summary_frame.pack(fill=tk.X, pady=10)

        ttk.Label(summary_frame, text=f"Account #{account_id}", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Type: {account['type'].capitalize()}").grid(row=1, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Opened: {account['created_at']}").grid(row=2, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Owner: {self.data['users'][account['owner']]['name']}").grid(row=3, column=0,
                                                                                                     sticky="w")

        ttk.Label(summary_frame, text="Current Balance:", font=('Arial', 12)).grid(row=1, column=1, sticky="e")
        ttk.Label(summary_frame, text=f"${account['balance']:.2f}", font=('Arial', 18, 'bold')).grid(row=2, column=1,
                                                                                                     sticky="e")

        # Transaction section
        transaction_frame = ttk.LabelFrame(main_frame, text="Make Transaction", padding=10)
        transaction_frame.pack(fill=tk.X, pady=10)

        # Transaction type
        ttk.Label(transaction_frame, text="Transaction Type:").grid(row=0, column=0, sticky="w", pady=5)
        transaction_type = tk.StringVar()
        type_combobox = ttk.Combobox(transaction_frame, textvariable=transaction_type, state="readonly")
        type_combobox['values'] = ('deposit', 'withdraw')
        type_combobox.current(0)
        type_combobox.grid(row=0, column=1, sticky="w", pady=5)

        # Amount
        ttk.Label(transaction_frame, text="Amount ($):").grid(row=1, column=0, sticky="w", pady=5)
        amount_var = tk.DoubleVar(value=0.0)
        amount_entry = ttk.Entry(transaction_frame, textvariable=amount_var, width=20)
        amount_entry.grid(row=1, column=1, sticky="w", pady=5)

        # Description
        ttk.Label(transaction_frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        description_entry = ttk.Entry(transaction_frame, width=40)
        description_entry.grid(row=2, column=1, sticky="w", pady=5)

        # Submit button
        submit_button = ttk.Button(
            transaction_frame,
            text="Submit Transaction",
            command=lambda: self.process_transaction(
                account_id,
                transaction_type.get(),
                amount_var.get(),
                description_entry.get(),
                detail_window  # Pass window to update it
            )
        )
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Transaction history section
        history_frame = ttk.LabelFrame(main_frame, text="Transaction History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create Treeview for transactions
        transaction_tree = ttk.Treeview(
            history_frame,
            columns=("date", "type", "amount", "description"),
            show="headings"
        )
        transaction_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Add scrollbar
        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=transaction_tree.yview)
        transaction_tree.configure(yscrollcommand=history_scroll.set)
        history_scroll.pack(side=tk.RIGHT, fill="y")

        # Define headings
        transaction_tree.heading("date", text="Date")
        transaction_tree.heading("type", text="Type")
        transaction_tree.heading("amount", text="Amount")
        transaction_tree.heading("description", text="Description")

        # Define column widths
        transaction_tree.column("date", width=150)
        transaction_tree.column("type", width=100)
        transaction_tree.column("amount", width=100)
        transaction_tree.column("description", width=200)

        # Populate transaction data (most recent first)
        for transaction in reversed(account['transactions']):
            transaction_tree.insert(
                "", "end",
                values=(
                    transaction['date'],
                    transaction['type'].capitalize(),
                    f"${transaction['amount']:.2f}" if transaction[
                                                           'type'] == 'deposit' else f"-${transaction['amount']:.2f}",
                    transaction['description']
                )
            )

        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=detail_window.destroy)
        close_button.pack(pady=10)

    def create_user(self, username, password, name, role):
        if not username or not password or not name:
            messagebox.showerror("Error", "All fields are required")
            return

        if username in self.data['users']:
            messagebox.showerror("Error", "Username already exists")
            return

        self.data['users'][username] = {
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'role': role,
            'name': name
        }

        self.save_data()
        messagebox.showinfo("Success", f"User {username} created successfully")

        # Refresh the admin dashboard to show the new user
        self.show_admin_dashboard()

    def create_account(self, owner, account_type, initial_balance):
        if not owner:
            messagebox.showerror("Error", "Please select an owner")
            return

        if initial_balance < 0:
            messagebox.showerror("Error", "Initial balance cannot be negative")
            return

        account_id = f"ACC{len(self.data['accounts']) + 1:06d}"

        self.data['accounts'][account_id] = {
            'owner': owner,
            'type': account_type,
            'balance': initial_balance,
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': [
                {
                    'type': 'deposit',
                    'amount': initial_balance,
                    'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'description': 'Initial deposit'
                }
            ]
        }

        self.save_data()
        messagebox.showinfo("Success", f"Account {account_id} created successfully")

        # Refresh the admin dashboard to show the new account
        self.show_admin_dashboard()

    def process_transaction(self, account_id, transaction_type, amount, description, window=None):
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero")
            return

        account = self.data['accounts'][account_id]

        if transaction_type == 'withdraw' and amount > account['balance']:
            messagebox.showerror("Error", "Insufficient funds")
            return

        if transaction_type == 'deposit':
            account['balance'] += amount
        elif transaction_type == 'withdraw':
            account['balance'] -= amount

        # Add transaction record
        account['transactions'].append({
            'type': transaction_type,
            'amount': amount,
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'description': description if description else f"{transaction_type.capitalize()} transaction"
        })

        self.save_data()
        messagebox.showinfo("Success", "Transaction completed successfully")

        # Refresh views
        if window:
            window.destroy()
            self.show_account_details(account_id)

        # If the current view is a client dashboard, refresh it
        if self.user_role == 'client':
            self.show_client_dashboard()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BankSystem()
    app.run()