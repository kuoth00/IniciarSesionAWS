import json
import os
from cryptography.fernet import Fernet

class AccountManager:
    def __init__(self, storage_file="accounts.json", key_file="secret.key"):
        self.storage_file = storage_file
        self.key_file = key_file
        self.key = self.load_or_generate_key()
        self.cipher_suite = Fernet(self.key)

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
            return key

    def save_account(self, name, account_id, username, password, region="us-east-1"):
        accounts = self.get_accounts()
        
        # Encrypt sensitive data
        encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()
        
        accounts[name] = {
            "account_id": account_id,
            "username": username,
            "password": encrypted_password,
            "region": region
        }
        
        with open(self.storage_file, "w") as f:
            json.dump(accounts, f, indent=4)

    def get_accounts(self):
        if not os.path.exists(self.storage_file):
            return {}
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def get_password(self, account_name):
        accounts = self.get_accounts()
        if account_name in accounts:
            encrypted_password = accounts[account_name]["password"]
            return self.cipher_suite.decrypt(encrypted_password.encode()).decode()
        return None
        
    def delete_account(self, account_name):
        accounts = self.get_accounts()
        if account_name in accounts:
            del accounts[account_name]
            with open(self.storage_file, "w") as f:
                json.dump(accounts, f, indent=4)
