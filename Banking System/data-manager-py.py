import os
import json
import hashlib
import datetime

class DataManager:
    def __init__(self, data_file='data/bank_data.json'):
        self.DATA_FILE = data_file
        self.data = self.load_data()
    
    def load_data(self):
        """Load data from JSON file or create default if file doesn't exist"""
        if not os.path.exists(self.DATA_FILE):
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
            
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
            return default_data
        else:
            # Load existing data
            with open(self.DATA_FILE, 'r') as f:
                return json.load(f)
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def authenticate_user(self, username, password):
        """Authenticate a user and return their role if successful"""
        if not username or not password:
            return None
        
        # Check if username exists and password matches
        if (username in self.data['users'] and
                self.data['users'][username]['password'] == hashlib.sha256(password.encode()).hexdigest()):
            return self.data['users'][username]['role']
        return None
    
    def get_user_data(self, username):
        """Get user data by username"""
        return self.data['users'].get(username)
    
    def get_users(self):
        """Get all users"""
        return self.data['users']
    
    def add_user(self, username, password, name, role):
        """Add a new user"""
        if username in self.data['users']:
            return False, "Username already exists"
        
        self.data['users'][username] = {
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'role': role,
            'name': name
        }
        self.save_data()
        return True, f"User {username} created successfully"
    
    def get_accounts(self):
        """Get all accounts"""
        return self.data['accounts']
    
    def get_user_accounts(self, username):
        """Get accounts belonging to a specific user"""
        return {acc_id: acc for acc_id, acc in self.data['accounts'].items() 
                if acc['owner'] == username}
    
    def create_account(self, owner, account_type, initial_balance):
        """Create a new account"""
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
        return account_id
    
    def get_account(self, account_id):
        """Get account by ID"""
        return self.data['accounts'].get(account_id)
    
    def process_transaction(self, account_id, transaction_type, amount, description):
        """Process a transaction (deposit or withdrawal)"""
        if amount <= 0:
            return False, "Amount must be greater than zero"
        
        account = self.data['accounts'].get(account_id)
        if not account:
            return False, "Account not found"
        
        if transaction_type == 'withdraw' and amount > account['balance']:
            return False, "Insufficient funds"
        
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
        return True, "Transaction completed successfully"
