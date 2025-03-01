# Web Blocker

Web Blocker is a desktop application developed using PyQt5 that enables users to block and unblock websites by modifying the `hosts` file. This application provides a user-friendly interface for managing blocked websites, adjusting settings, and enforcing access control through simple math problems.

# Patch Log

## v1.1.0 - 2024-07-21

### New Features
- **Application Icon**: The application now uses its own icon (`app.ico`) for the window and taskbar.
- **Customizable Removal Behavior**: Added a new setting in the settings dialog to enable or disable the removal of all websites containing a specific phrase. This can be toggled via the "Remove all matching websites" checkbox.
- **Duplicate Website Check**: The application now prevents adding websites that are already in the blocked list, ensuring no duplicates are added.

### Enhancements
- **Settings Translation**: Updated the settings to include translations for the new "Remove all matching websites" option in English, Polish, and German.

### Bug Fixes
- None in this release.

### Technical Improvements
- Modified the `main.py` to set the application icon during initialization.
- Updated the `ui.py` to include the new checkbox in the settings dialog and align the checkboxes and labels to the left for better UI consistency.
- Enhanced the `add_website` method to check for duplicates before adding new websites to the blocked list.

### Known Issues
- Custum URL forwarder can sometimes cause websites unblocking.

### How to Update
1. Pull the latest changes from the repository.
2. Install any new dependencies using `pip install -r requirements.txt`.
3. Rebuild the application using the updated PyInstaller spec file if compiling to an executable.

## Features

- **Block and Unblock Websites**: Easily manage which websites are blocked or accessible.
- **Manage Blocked Websites**: Add or remove websites from the blocked list.
- **Customizable Settings**:
  - **Math Problems**: Set the number of math problems required to access certain features.
  - **Redirect IP**: Specify the IP address to which blocked websites will be redirected (default is `127.0.0.1`).
  - **Language**: Choose the interface language (English, Polish, or German).
- **Restore Defaults**: Restore the application to its default settings or retrieve blocked websites from the `hosts` file.

## Installation

1. Navigate to the project directory:
   ```sh
   cd web-blocker
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```sh
python main.py
```

The application will prompt for administrative privileges to modify the `hosts` file. Use the provided buttons to block or unblock websites, manage blocked websites, or access settings.

## File Structure

- `main.py`: Main application file.
- `blocked_websites.txt`: File storing the list of blocked websites.
- `style.qss`: Stylesheet for the application's UI.
- `icons/shield_icon.png`: Icon for the application.

## Configuration

The application allows users to customize the following settings:

- **Math Problems**: Number of math problems required to access certain features.
- **Redirect IP**: IP address to redirect blocked websites to (default is `127.0.0.1`).
- **Language**: Interface language (English, Polish, or German).

## Screenshots

### Main Screen
![image](https://github.com/user-attachments/assets/238528bb-f991-45fa-8848-32bad498a02f)

### Settings
![image](https://github.com/user-attachments/assets/0d8b80a0-37ec-4777-88b5-dcf6447c83a2)

### Manage Websites
![image](https://github.com/user-attachments/assets/b21cba48-6a2b-49ba-82ce-814e3845b988)

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes.
4. Commit your changes:
   ```sh
   git commit -m "Add feature"
   ```
5. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
6. Open a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- **PyQt5**: For providing the framework to build the UI.
- **Contributors**: And the open-source community for their support.
```

Ten opis zawiera wszystkie istotne informacje o projekcie, instrukcje instalacji i używania, oraz informacje o strukturze plików, co powinno być pomocne dla użytkowników i współtwórców projektu.
