import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from account_manager import AccountManager

# Set theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# AWS Colors
AWS_ORANGE = "#FF9900"
AWS_HOVER = "#FFAC31"
DARK_BG = "#232F3E"  # AWS Console Dark Header
LIGHTER_BG = "#37475A" # Lighter standard grey

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.account_manager = AccountManager()

        # Configure window
        self.title("AWS Console Login")
        self.geometry("700x550")

        # Layout grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0, fg_color=DARK_BG)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="AWS Login 🚀", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.add_account_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="+ Add Account",
            font=ctk.CTkFont(size=13, weight="bold"), 
            command=self.add_account_event,
            fg_color=AWS_ORANGE,
            hover_color=AWS_HOVER,
            text_color="black",
            height=35
        )
        self.add_account_btn.grid(row=1, column=0, padx=20, pady=10)

        # Main area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1) # Row 2 takes space
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="Your Accounts", 
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="w")

        # Search Bar
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_search)
        self.search_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="🔍 Search accounts...", 
            textvariable=self.search_var,
            width=300,
            height=35
        )
        self.search_entry.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="w")

        # Account list
        self.account_list_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.account_list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        self.refresh_account_list()

    def update_search(self, *args):
        self.refresh_account_list(filter_text=self.search_var.get())

    def refresh_account_list(self, filter_text=""):
        # Clear existing
        for widget in self.account_list_frame.winfo_children():
            widget.destroy()
            
        accounts = self.account_manager.get_accounts()
        
        # Filter
        filtered_accounts = {k: v for k, v in accounts.items() if filter_text.lower() in k.lower() or filter_text.lower() in v.get('account_id', '')}
        
        if not filtered_accounts:
            lbl = ctk.CTkLabel(self.account_list_frame, text="No accounts found.", text_color="gray")
            lbl.pack(pady=40)
            return

        for name, data in filtered_accounts.items():
            self.create_account_card(name, data)

    def create_account_card(self, name, data):
        card = ctk.CTkFrame(self.account_list_frame, fg_color=LIGHTER_BG, corner_radius=10)
        card.pack(fill="x", pady=6, padx=10)
        
        # Info container
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=15, pady=12, fill="both", expand=True)

        lbl_name = ctk.CTkLabel(info_frame, text=name, font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color="white")
        lbl_name.pack(anchor="w")
        
        lbl_id = ctk.CTkLabel(info_frame, text=f"ID: {data['account_id']} | User: {data.get('username', 'N/A')}", font=ctk.CTkFont(size=11), text_color="#AAB7B8")
        lbl_id.pack(anchor="w")

        # Buttons container
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=15, pady=12)

        btn_login = ctk.CTkButton(
            btn_frame, 
            text="Login 🚀", 
            width=80,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda n=name: self.login_event(n),
            fg_color=AWS_ORANGE,
            hover_color=AWS_HOVER,
            text_color="black"
        )
        btn_login.pack(side="right", padx=5)

        # Edit button (just re-open add dialog with pre-fill)
        btn_edit = ctk.CTkButton(
            btn_frame,
            text="✏️",
            width=35,
            height=32,
            fg_color="#405060",
            hover_color="#506070",
            command=lambda n=name: self.add_account_event(edit_name=n)
        )
        btn_edit.pack(side="right", padx=5)

        btn_delete = ctk.CTkButton(
            btn_frame,
            text="🗑️",
            width=35,
            height=32,
            fg_color="#D13212", # Red
            hover_color="#B22205",
            command=lambda n=name: self.delete_account_event(n)
        )
        btn_delete.pack(side="right", padx=5)

    def delete_account_event(self, account_name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{account_name}'?"):
            self.account_manager.delete_account(account_name)
            self.refresh_account_list(filter_text=self.search_var.get())

    def add_account_event(self, edit_name=None):
        title = "Add AWS Account"
        if edit_name:
            title = f"Edit {edit_name}"

        # Create a top-level window for adding account
        add_window = ctk.CTkToplevel(self)
        add_window.title(title)
        add_window.geometry("400x480")
        add_window.grab_set() # Make modal
        
        # Container
        frame = ctk.CTkFrame(add_window, fg_color="transparent")
        frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Helper to get existing data if editing
        existing_data = {}
        existing_pass = ""
        if edit_name:
            existing_data = self.account_manager.get_accounts().get(edit_name, {})
            existing_pass = self.account_manager.get_password(edit_name)

        ctk.CTkLabel(frame, text="New Account Details", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 20))
        
        ctk.CTkLabel(frame, text="Account Alias", anchor="w").pack(fill="x", pady=(5,0))
        entry_name = ctk.CTkEntry(frame)
        entry_name.pack(fill="x", pady=5)
        if edit_name: 
            entry_name.insert(0, edit_name)
            entry_name.configure(state="disabled") # Disabled renaming for simplicity key management
        
        ctk.CTkLabel(frame, text="AWS Account ID", anchor="w").pack(fill="x", pady=(5,0))
        entry_id = ctk.CTkEntry(frame)
        entry_id.pack(fill="x", pady=5)
        if edit_name: entry_id.insert(0, existing_data.get("account_id", ""))

        ctk.CTkLabel(frame, text="IAM Username", anchor="w").pack(fill="x", pady=(5,0))
        entry_user = ctk.CTkEntry(frame)
        entry_user.pack(fill="x", pady=5)
        if edit_name: entry_user.insert(0, existing_data.get("username", ""))
        
        ctk.CTkLabel(frame, text="Password", anchor="w").pack(fill="x", pady=(5,0))
        entry_pass = ctk.CTkEntry(frame, show="*")
        entry_pass.pack(fill="x", pady=5)
        if edit_name: entry_pass.insert(0, existing_pass)
        
        def save():
            name = entry_name.get()
            acc_id = entry_id.get()
            user = entry_user.get()
            pwd = entry_pass.get()
            
            if name and acc_id and user and pwd:
                self.account_manager.save_account(name, acc_id, user, pwd)
                add_window.destroy()
                self.refresh_account_list(filter_text=self.search_var.get())
            else:
                messagebox.showwarning("Incomplete", "Please fill in all fields.")

        ctk.CTkButton(
            frame, 
            text="Save Account", 
            command=save,
            fg_color=AWS_ORANGE,
            hover_color=AWS_HOVER,
            text_color="black",
            height=40
        ).pack(pady=30, fill="x")
    
    def login_event(self, account_name):
        print(f"Logging in to {account_name}")
        account = self.account_manager.get_accounts().get(account_name)
        if not account:
            messagebox.showerror("Error", "Account not found!")
            return

        password = self.account_manager.get_password(account_name)
        if not password:
            messagebox.showerror("Error", "Could not decrypt password!")
            return

        try:
            # Setup Chrome options
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True) # Keep browser open
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled") # Help avoid detection
            
            # Initialize Driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            # Go to AWS Console
            # Using specific signin URL to force standard flow if possible
            driver.get("https://signin.aws.amazon.com/console")
            
            wait = WebDriverWait(driver, 20)
            
            def find_any(selectors):
                for by, pattern in selectors:
                    try:
                        elem = driver.find_element(by, pattern)
                        if elem.is_displayed():
                            return elem
                    except:
                        continue
                return None

            # --- STEP 1: RESOLVE ACCOUNT (Root vs IAM) ---
            print("Step 1: finding account input...")
            
            # Try to handle "IAM User" selection if radio buttons exist
            try:
                iam_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'IAM user')]")))
                iam_label.click()
                print("Clicked IAM User label")
            except:
                pass # Maybe not present, or already selected

            # Wait for meaningful input
            time.sleep(2) # brief pause for animations
            
            # Try multiple selectors for the first input field (Account ID or Email)
            account_selectors = [
                 (By.ID, "resolving_input"),
                 (By.ID, "account"),
                 (By.NAME, "account"),
                 (By.CSS_SELECTOR, "input[type='text']"),
                 (By.CSS_SELECTOR, "input[type='email']")
            ]
            
            account_field = None
            try:
                 # Wait for at least one input to be present
                 wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
                 account_field = find_any(account_selectors)
            except:
                pass
                
            if account_field:
                account_field.clear()
                account_field.send_keys(account["account_id"])
                print("Entered Account ID / Email")
                
                # Find Next button
                next_btn = find_any([(By.ID, "next_button"), (By.ID, "next_button_text"), (By.CSS_SELECTOR, "button[type='submit']")])
                if next_btn:
                    next_btn.click()
                    print("Clicked Next")
            else:
                print("Could not find Account ID field. User might need to enter manually.")
            
            # --- STEP 2: USERNAME & PASSWORD ---
            # Wait for redirection or form update
            try:
                # Wait for username field
                wait.until(EC.visibility_of_element_located((By.ID, "username")))
                
                user_field = driver.find_element(By.ID, "username")
                user_field.clear()
                user_field.send_keys(account["username"])
                print("Entered Username")
                
                pass_field = driver.find_element(By.ID, "password")
                pass_field.clear()
                pass_field.send_keys(password)
                print("Entered Password")
                
                signin_btn = driver.find_element(By.ID, "signin_button")
                signin_btn.click()
                print("Clicked Sign In")
                
            except Exception as e:
                print(f"Step 2 (User/Pass) issue: {e}")
                # Sometimes it goes straight to password if username was inferred?
                pass

        except Exception as e:
            err_msg = f"Automation error: {str(e)}"
            print(err_msg)
            # Don't show popup aggressively, let user see console

if __name__ == "__main__":
    app = App()
    app.mainloop()
