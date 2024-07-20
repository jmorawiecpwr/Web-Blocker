# Web Blocker Application

Web Blocker is a PyQt5-based desktop application that allows users to block and unblock websites. The app supports multiple languages (English, Polish, and German) and includes settings for managing blocked websites, redirect IP addresses, and math problems to ensure authorized access to settings and website management.

## Features

- **Block and Unblock Websites**: Easily block and unblock websites through the application's interface.
- **Manage Blocked Websites**: Add or remove websites from the blocking list.
- **Settings**: Customize the number of math problems required for access, redirect IP address, and language settings.
- **Multi-language Support**: Available in English, Polish, and German.
- **Math Problems**: Users must solve math problems to access settings or unblock websites.

## Important Notes

- **Hosts File Modification**: The program modifies the `hosts` file to block or unblock websites. Uninstalling the application will not automatically unblock any previously blocked websites.
- **Delayed Changes**: The process of blocking and unblocking websites might experience delays, especially with frequent changes to the blocking list. 
- **Temporary List Management**: The list of websites to be blocked or unblocked is maintained temporarily and may not reflect immediate changes to the `hosts` file. To ensure the list is accurate, use the "Restore from hosts" button to view the current contents of the `hosts` file in case of accidental deletion.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/web-blocker.git
2. Navigate to the project directory:
```sh
cd web-blocker
3. Install the required dependencies:
pip install -r requirements.txt
4. Usage
Run the application:
python main.py
The application will prompt for administrative privileges to modify the hosts file.
Use the buttons to block or unblock websites, manage blocked websites, or access settings.

File Structure
main.py: Main application file.
blocked_websites.txt: File storing the list of blocked websites.
style.qss: Stylesheet for the application's UI.
icons/shield_icon.png: Icon for the application.
Configuration
The application allows users to customize the following settings:

Math Problems: Number of math problems required to access certain features.
Redirect IP: IP address to redirect blocked websites to (default is 127.0.0.1).
Language: Interface language (English, Polish, or German).
