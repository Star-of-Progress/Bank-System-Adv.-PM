import tkinter as tk
from tkinter import ttk, messagebox

class AccountDetailsWindow:
    def __init__(self, parent, data_manager, account_id, user_role, current_user, refresh_callback=None):
        self.parent = parent
        self.data_manager = data_manager
        self.account_id = account_id
        self.user_role = user_role
        self.current_user = current_user
        self.refresh_callback = refresh_callback
        
        account = self.data_manager.get_account(account_id)
        if not account:
            messagebox.showerror("Error", "Account does not exist")
            return
        
        # Check if current user is admin or the account owner
        if self.user_role != 'admin' and account['owner'] != self.current_user:
            messagebox.showerror("Error", "You don't have permission to view this account")
            return
        
        self.account = account
        self.setup_window()
    
    def setup_window(self):
        # Create a new window for account details
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Account Details - {self.account_id}")
        self.window.geometry("700x500")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Account summary section
        self._setup_summary_section(main_frame)
        
        # Transaction section
        self._setup_transaction_section(main_frame)
        
        # Transaction history section
        self._setup_history_section(main_frame)
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.window.destroy)
        close_button.pack(pady=10)
    
    def _setup_summary_section(self, parent):
        summary_frame = ttk.Frame(parent, padding=10)
        summary_frame.pack(fill=tk.X, pady=10)
        
        owner_name = self.data_manager.get_user_data(self.account['owner'])['name']
        
        ttk.Label(summary_frame, text=f"Account #{self.account_id}", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Type: {self.account['type'].capitalize()}").grid(row=1, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Opened: {self.account['created_at']}").grid(row=2, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Owner: {owner_name}").grid(row=3, column=0, sticky="w")
        
        ttk.Label(summary_frame, text="Current Balance:", font=('Arial', 12)).grid(row=1, column=1, sticky="e")
        ttk.Label(summary_frame, text=f"${self.account['balance']:.2f}", font=('Arial', 18, 'bold')).grid(row=2, column=1, sticky="e")
    
    def _setup_transaction_section(self, parent):
        transaction_frame = ttk.LabelFrame(parent, text="Make Transaction", padding=10)
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
            command=lambda: self._process_transaction(
                transaction_type.get(),
                amount_var.get(),
                description_entry.get()
            )
        )
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def _setup_history_section(self, parent):
        history_frame = ttk.LabelFrame(parent, text="Transaction History", padding=10)
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
        