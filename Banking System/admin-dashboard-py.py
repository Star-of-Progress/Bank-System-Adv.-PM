import tkinter as tk
from tkinter import ttk, messagebox

class AdminDashboard:
    def __init__(self, master, data_manager, user_data, logout_callback, show_account_details_callback):
        self.master = master
        self.data_manager = data_manager
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
        
        # Create a notebook (tab control)
        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # User Management Tab
        user_frame = ttk.Frame(notebook, padding=10)
        notebook.add(user_frame, text="User Management")

        # Account Management Tab
        account_frame = ttk.Frame(notebook, padding=10)
        notebook.add(account_frame, text="Account Management")

        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        welcome_label = ttk.Label(
            header_frame,
            text=f"Welcome, {self.user_data['name']} (Admin)"
        )
        welcome_label.pack(side=tk.LEFT)

        logout_button = ttk.Button(header_frame, text="Logout", command=self.logout_callback)
        logout_button.pack(side=tk.RIGHT)

        # USER MANAGEMENT TAB CONTENT
        self._setup_user_management_tab(user_frame)
        
        # ACCOUNT MANAGEMENT TAB CONTENT
        self._setup_account_management_tab(account_frame)

    def _setup_user_management_tab(self, frame):
        # Create new user form
        ttk.Label(frame, text="Create New User", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        user_form_frame = ttk.Frame(frame)
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
            command=lambda: self._create_user(
                username_entry.get(),
                password_entry.get(),
                name_entry.get(),
                role_var.get()
            )
        )
        create_user_button.grid(row=4, column=0, columnspan=2, pady=10)

        # User List
        ttk.Label(frame, text="User List", style="Header.TLabel").pack(anchor="w", pady=(20, 10))

        # Create Treeview for user list
        user_tree = ttk.Treeview(frame, columns=("username", "name", "role"), show="headings")
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
        for username, user_data in self.data_manager.get_users().items():
            user_tree.insert("", "end", values=(username, user_data['name'], user_data['role']))

    def _setup_account_management_tab(self, frame):
        # Create new account form
        ttk.Label(frame, text="Create New Account", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        account_form_frame = ttk.Frame(frame)
        account_form_frame.pack(fill=tk.X, pady=10)

        # Owner (Client) dropdown
        ttk.Label(account_form_frame, text="Owner (Client):").grid(row=0, column=0, sticky="w", pady=5)
        owner_var = tk.StringVar()
        owner_combobox = ttk.Combobox(account_form_frame, textvariable=owner_var, state="readonly")

        # Populate with client users only
        client_users = [(username, user['name']) for username, user in self.data_manager.get_users().items()
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
            command=lambda: self._create_account(
                owner_var.get().split('(')[1].split(')')[0] if owner_var.get() else "",
                type_var.get(),
                balance_var.get()
            )
        )
        create_account_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Account List
        ttk.Label(frame, text="Account List", style="Header.TLabel").pack(anchor="w", pady=(20, 10))

        # Create Treeview for account list
        account_tree = ttk.Treeview(
            frame,
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
                        lambda event: self.show_account_details_callback(
                            account_tree.item(account_tree.focus())["values"][0]))

        # Populate account data
        for account_id, account_data in self.data_manager.get_accounts().items():
            owner_name = self.data_manager.get_user_data(account_data['owner'])['name']
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

    def _create_user(self, username, password, name, role):
        if not username or not password or not name:
            messagebox.showerror("Error", "All fields are required")
            return
        
        success, message = self.data_manager.add_user(username, password, name, role)
        if success:
            messagebox.showinfo("Success", message)
            self.show()  # Refresh the view
        else:
            messagebox.showerror("Error", message)

    def _create_account(self, owner, account_type, initial_balance):
        if not owner:
            messagebox.showerror("Error", "Please select an owner")
            return
        
        if initial_balance < 0:
            messagebox.showerror("Error", "Initial balance cannot be negative")
            return
        
        account_id = self.data_manager.create_account(owner, account_type, initial_balance)
        messagebox.showinfo("Success", f"Account {account_id} created successfully")
        self.show()  # Refresh the view
