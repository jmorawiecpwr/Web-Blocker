import os
import sys
import ctypes
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QListWidget, QMessageBox, QInputDialog, QWidget, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from settings import languages, default_redirect_ip, hosts_path, blocked_websites_file
from logic import Logic

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = {"math_problems": 0, "redirect_ip": default_redirect_ip, "language": "English", "add_prefixes": False}
        self.language = languages[self.settings["language"]]
        self.logic = Logic(self.settings)

        self.initUI()
        self.update_buttons()

    def initUI(self):
        self.setWindowTitle(self.language["title"])
        self.setGeometry(100, 100, 400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(QPixmap(self.resource_path("icons/shield_icon.png")).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
        title_layout.addWidget(title_icon)
        title_label = QLabel(self.language["title"])
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        title_layout.addWidget(title_label)
        title_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(title_layout)

        self.block_button = QPushButton()
        self.block_button.setObjectName("blockButton")
        self.block_button.clicked.connect(self.toggle_blocking)
        layout.addWidget(self.block_button)

        self.settings_button = QPushButton(self.language["settings"])
        self.settings_button.setObjectName("mainButton")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)

        self.manage_websites_button = QPushButton(self.language["manage_websites"])
        self.manage_websites_button.setObjectName("mainButton")
        self.manage_websites_button.clicked.connect(self.manage_websites)
        layout.addWidget(self.manage_websites_button)

        central_widget.setLayout(layout)

        self.load_stylesheet(self.resource_path("style.qss"))

    def load_stylesheet(self, style_file):
        with open(style_file, "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run_as_admin(self):
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()

    def is_admin(self):
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def toggle_blocking(self):
        if self.logic.check_websites_blocked():
            if self.logic.check_math_problems():
                self.logic.modify_hosts_file(block=False)
                self.update_buttons()
        else:
            self.logic.modify_hosts_file(block=True)
            self.update_buttons()

    def open_settings(self):
        if self.logic.check_math_problems():
            self.open_custom_settings()

    def open_custom_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.language["settings"])
        dialog.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        math_problems_label = QLabel(self.language["math_problems"])
        layout.addWidget(math_problems_label)

        math_problems_input = QLineEdit()
        math_problems_input.setText(str(self.settings["math_problems"]))
        layout.addWidget(math_problems_input)

        redirect_ip_label = QLabel(self.language["redirect_ip"])
        layout.addWidget(redirect_ip_label)

        redirect_ip_input = QLineEdit()
        redirect_ip_input.setText(self.settings["redirect_ip"])
        layout.addWidget(redirect_ip_input)

        language_label = QLabel("Language:")
        layout.addWidget(language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItems(languages.keys())
        self.language_combo.setCurrentText(self.settings["language"])
        layout.addWidget(self.language_combo)

        add_prefixes_layout = QHBoxLayout()
        self.add_prefixes_checkbox = QCheckBox()
        self.add_prefixes_checkbox.setChecked(self.settings["add_prefixes"])
        add_prefixes_label = QLabel("Add common subdomains (www, pl, en, de, etc.):")
        add_prefixes_layout.addWidget(self.add_prefixes_checkbox)
        add_prefixes_layout.addWidget(add_prefixes_label)
        add_prefixes_layout.setAlignment(QtCore.Qt.AlignLeft)
        layout.addLayout(add_prefixes_layout)

        remove_all_matches_layout = QHBoxLayout()
        self.remove_all_matches_checkbox = QCheckBox()
        self.remove_all_matches_checkbox.setChecked(self.settings.get("remove_all_matches", False))
        remove_all_matches_label = QLabel(self.language["remove_all_matches"])
        remove_all_matches_layout.addWidget(self.remove_all_matches_checkbox)
        remove_all_matches_layout.addWidget(remove_all_matches_label)
        remove_all_matches_layout.setAlignment(QtCore.Qt.AlignLeft)
        layout.addLayout(remove_all_matches_layout)

        buttons_layout = QHBoxLayout()

        ok_button = QPushButton("OK")
        ok_button.setObjectName("dialogButton")
        ok_button.clicked.connect(
            lambda: self.save_settings(dialog, math_problems_input.text(), redirect_ip_input.text(),
                                       self.add_prefixes_checkbox.isChecked(),
                                       self.remove_all_matches_checkbox.isChecked()))
        buttons_layout.addWidget(ok_button)

        restore_default_button = QPushButton(self.language["restore_default"])
        restore_default_button.setObjectName("dialogButton")
        restore_default_button.clicked.connect(lambda: redirect_ip_input.setText(default_redirect_ip))
        buttons_layout.addWidget(restore_default_button)

        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)

        dialog.exec_()
    def save_settings(self, dialog, math_problems, redirect_ip, add_prefixes, remove_all_matches):
        try:
            self.settings["math_problems"] = int(math_problems)
        except ValueError:
            self.settings["math_problems"] = 0
        self.settings["redirect_ip"] = redirect_ip.strip() or default_redirect_ip
        self.settings["language"] = self.language_combo.currentText()
        self.settings["add_prefixes"] = add_prefixes
        self.settings["remove_all_matches"] = remove_all_matches
        dialog.accept()
        self.update_language()

    def update_language(self):
        self.language = languages[self.settings["language"]]
        self.setWindowTitle(self.language["title"])
        self.update_buttons()
        self.settings_button.setText(self.language["settings"])
        self.manage_websites_button.setText(self.language["manage_websites"])

    def update_buttons(self):
        if self.logic.check_websites_blocked():
            self.block_button.setText("Websites are blocked")
            self.block_button.setStyleSheet("background-color: #ff6666; color: white;")
        else:
            self.block_button.setText("Websites are unblocked")
            self.block_button.setStyleSheet("background-color: #28a745; color: white;")

    def manage_websites(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.language["manage_websites"])
        dialog.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        list_label = QLabel(self.language["manage_blocked_websites"])
        layout.addWidget(list_label)

        self.website_list = QListWidget()
        self.update_website_list()
        layout.addWidget(self.website_list)

        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText(self.language["no_website_entered"])
        layout.addWidget(self.website_input)

        buttons_layout = QHBoxLayout()

        add_button = QPushButton(self.language["add"])
        add_button.setObjectName("dialogButton")
        add_button.clicked.connect(lambda: self.add_website(self.website_input.text()))
        buttons_layout.addWidget(add_button)

        remove_button = QPushButton(self.language["remove"])
        remove_button.setObjectName("dialogButton")
        remove_button.clicked.connect(lambda: self.remove_selected_website())
        buttons_layout.addWidget(remove_button)

        restore_button = QPushButton(self.language["restore_from_hosts"])
        restore_button.setObjectName("dialogButton")
        restore_button.clicked.connect(lambda: self.restore_from_hosts())
        buttons_layout.addWidget(restore_button)

        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)

        dialog.exec_()

    def update_website_list(self):
        self.website_list.clear()
        blocked_websites = self.logic.load_blocked_websites()
        self.website_list.addItems(blocked_websites)

    def add_website(self, website):
        if website:
            websites_to_add = [website]
            if self.settings.get("add_prefixes", False):
                prefixes = ["www", "pl", "en", "de"]
                websites_to_add.extend([f"{prefix}.{website}" for prefix in prefixes])
            blocked_websites = self.logic.load_blocked_websites()
            # Check for duplicates
            websites_to_add = [site for site in websites_to_add if site not in blocked_websites]
            if not websites_to_add:
                QMessageBox.information(self, self.language["error"], f"{website} is already in the list.")
                return
            blocked_websites.extend(websites_to_add)
            self.logic.save_blocked_websites(blocked_websites)
            self.update_website_list()
    def remove_selected_website(self):
        website_input = self.website_input.text().strip()
        selected_item = self.website_list.currentItem()
        if website_input:
            self.logic.remove_websites_containing(website_input)
        elif selected_item:
            pattern = selected_item.text()
            self.logic.remove_websites_containing(pattern)
        self.update_website_list()

    def restore_from_hosts(self):
        try:
            with open(hosts_path, 'r') as file:
                lines = file.readlines()
            blocked_websites = self.logic.load_blocked_websites()
            for line in lines:
                if line.startswith(self.settings["redirect_ip"]):
                    website = line.split()[1]
                    if website not in blocked_websites:
                        blocked_websites.append(website)
            self.logic.save_blocked_websites(blocked_websites)
            self.update_website_list()
        except Exception as e:
            QMessageBox.critical(self, self.language["error"], str(e))