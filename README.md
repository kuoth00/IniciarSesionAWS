# AWS Console Login Automator 🚀

A modern, secure, and efficient desktop application to manage and automate logins for multiple AWS accounts. Built with **Python**, **CustomTkinter** for the UI, and **Selenium** for browser automation.

![AWS Login App](https://via.placeholder.com/800x500?text=App+Screenshot+Placeholder)

## Features

*   **✨ Modern UI**: Clean, dark-themed interface with filterable search and account cards.
*   **🔒 Secure**: Encrypts stored passwords locally using `cryptography` (Fernet).
*   **⚡ Automated Login**: Opens Chrome and logs you straight into the AWS Console, handling the tricky redirects.
*   **📂 Multi-Account**: Manage unlimited accounts (Aliases, IDs, Users).
*   **🖱️ One-Click**: Launch any account with a single click.

## Installation

### Option 1: Standalone Executable (Windows)
No Python installed? No problem.
1.  Download the latest release (or check the `dist/` folder if you built it).
2.  Run `AWSLogin.exe`.

### Option 2: Run from Source
1.  **Clone the repo**:
    ```bash
    git clone https://github.com/yourusername/aws-login-automator.git
    cd aws-login-automator
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run**:
    ```bash
    python main.py
    ```
    *(Or use `run_app.bat` on Windows)*

## Usage

1.  **Add Account**: Click `+ Add Account` and fill in your AWS Alias/ID, IAM Username, and Password.
2.  **Search**: Use the search bar to find the specific environment (e.g., "Production").
3.  **Login**: Click the Rocket 🚀 button. Chrome will open and log you in automatically.

## Security Note ⚠️

This application stores your AWS passwords in a local file (`accounts.json`). While they are encrypted using a generated key (`secret.key`), **anyone with access to your computer and that key** can theoretically decrypt them.
*   Do not share your `accounts.json` or `secret.key`.
*   Ensure `.gitignore` is set up correctly (it is included in this repo) to prevent accidental upload of credentials.

## Technologies

*   [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - UI Library
*   [Selenium](https://www.selenium.dev/) - Browser Automation
*   [Cryptography](https://cryptography.io/en/latest/) - Encryption

---
*Created for personal productivity.*
