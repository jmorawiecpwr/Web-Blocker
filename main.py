import sys
import random
import os
import ctypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QDialog,
                             QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog, QMessageBox, QWidget, QComboBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
default_redirect_ip = "127.0.0.1"
blocked_websites_file = "blocked_websites.txt"

languages = {
    "English": {
        "title": "Web blocker",
        "block_websites": "Block websites",
        "unblock_websites": "Unblock websites",
        "settings": "Settings",
        "manage_websites": "Manage websites",
        "math_problems": "Enter number of math problems required:",
        "redirect_ip": "Redirect IP address for blocked websites:",
        "restore_default": "Restore default",
        "restore_from_hosts": "Restore from hosts",
        "error": "Error",
        "wrong_answer": "Wrong answer. Access denied.",
        "not_enough_correct": "Not enough correct answers.",
        "blocking_list_empty": "The blocking list is empty.",
        "no_website_entered": "No website entered.",
        "manage_blocked_websites": "Manage blocked websites",
        "add": "Add",
        "remove": "Remove",
        "math_problem": "Math Problem",
        "solve": "Solve:"
    },
    "Polski": {
        "title": "Blokada stron",
        "block_websites": "Blokuj strony",
        "unblock_websites": "Odblokuj strony",
        "settings": "Ustawienia",
        "manage_websites": "Zarządzaj stronami",
        "math_problems": "Wprowadź liczbę zadań matematycznych:",
        "redirect_ip": "Adres IP przekierowania dla zablokowanych stron:",
        "restore_default": "Przywróć domyślne",
        "restore_from_hosts": "Przywróć z hosts",
        "error": "Błąd",
        "wrong_answer": "Zła odpowiedź. Odmowa dostępu.",
        "not_enough_correct": "Nie wystarczająca liczba poprawnych odpowiedzi.",
        "blocking_list_empty": "Lista blokowanych stron jest pusta.",
        "no_website_entered": "Nie wprowadzono strony.",
        "manage_blocked_websites": "Zarządzaj zablokowanymi stronami",
        "add": "Dodaj",
        "remove": "Usuń",
        "math_problem": "Zadanie matematyczne",
        "solve": "Rozwiąż:"
    },
    "Deutsch": {
        "title": "Webblocker",
        "block_websites": "Webseiten blockieren",
        "unblock_websites": "Webseiten entsperren",
        "settings": "Einstellungen",
        "manage_websites": "Webseiten verwalten",
        "math_problems": "Geben Sie die Anzahl der Matheaufgaben ein:",
        "redirect_ip": "Umleitungs-IP-Adresse für blockierte Webseiten:",
        "restore_default": "Standard wiederherstellen",
        "restore_from_hosts": "Aus hosts wiederherstellen",
        "error": "Fehler",
        "wrong_answer": "Falsche Antwort. Zugriff verweigert.",
        "not_enough_correct": "Nicht genügend richtige Antworten.",
        "blocking_list_empty": "Die Blockierliste ist leer.",
        "no_website_entered": "Keine Webseite eingegeben.",
        "manage_blocked_websites": "Verwalten blockierter Webseiten",
        "add": "Hinzufügen",
        "remove": "Entfernen",
        "math_problem": "Matheaufgabe",
        "solve": "Lösen:"
    }
}

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = {"math_problems": 0, "redirect_ip": default_redirect_ip, "language": "English"}
        self.language = languages[self.settings["language"]]

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
        title_icon.setPixmap(QPixmap("icons/shield_icon.png").scaled(50, 50, QtCore.Qt.KeepAspectRatio))
        title_layout.addWidget(title_icon)
        title_label = QLabel(self.language["title"])
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        title_layout.addWidget(title_label)
        title_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(title_layout)

        self.block_button = QPushButton(self.language["block_websites"])
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

        self.load_stylesheet("style.qss")

    def load_stylesheet(self, style_file):
        with open(style_file, "r") as file:
            stylesheet = file.read()
            stylesheet = stylesheet.replace("cursor:", "")
            stylesheet = stylesheet.replace("transition:", "")
            self.setStyleSheet(stylesheet)

    def is_admin(self):
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def run_as_admin(self):
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()

    def modify_hosts_file(self, block=True):
        try:
            with open(hosts_path, 'r+') as file:
                content = file.read()
                websites_to_block = self.load_blocked_websites()
                if block:
                    if not websites_to_block:
                        QMessageBox.critical(self, self.language["error"], self.language["blocking_list_empty"])
                        return
                    for website in websites_to_block:
                        if website not in content:
                            file.write(f"{self.settings['redirect_ip']} {website}\n")
                            print(f"{website} has been blocked.")
                else:
                    file.seek(0)
                    new_content = [line for line in content.splitlines() if not any(website in line for website in websites_to_block)]
                    file.truncate(0)
                    file.write("\n".join(new_content))
                    print("Blocks have been removed.")
        except PermissionError:
            print("Permission denied to modify hosts file. Run the script as an administrator.")
        except FileNotFoundError:
            print(f"Hosts file not found: {hosts_path}")
        except Exception as e:
            print(f"Failed to modify hosts file: {e}")

    def load_blocked_websites(self):
        if os.path.exists(blocked_websites_file):
            with open(blocked_websites_file, 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    def save_blocked_websites(self, websites):
        with open(blocked_websites_file, 'w') as file:
            for website in websites:
                file.write(f"{website}\n")

    def toggle_blocking(self):
        if self.check_websites_blocked():
            if self.check_math_problems():
                self.modify_hosts_file(block=False)
                self.update_buttons()
        else:
            self.modify_hosts_file(block=True)
            self.update_buttons()

    def check_websites_blocked(self):
        try:
            with open(hosts_path, 'r') as file:
                content = file.read()
            websites_to_block = self.load_blocked_websites()
            return any(website in content for website in websites_to_block)
        except FileNotFoundError:
            return False

    def check_math_problems(self):
        problems_needed = self.settings["math_problems"]
        correct_answers = 0

        for _ in range(problems_needed):
            question, answer = self.generate_math_problem()
            user_answer, ok = QInputDialog.getInt(self, self.language["math_problem"], f"{self.language['solve']} {question}")
            if ok and user_answer == answer:
                correct_answers += 1
            else:
                QMessageBox.critical(self, self.language["error"], self.language["wrong_answer"])
                return False

        if correct_answers == problems_needed:
            return True
        else:
            QMessageBox.critical(self, self.language["error"], self.language["not_enough_correct"])
            return False

    def generate_math_problem(self):
        num1 = random.randint(1, 99)
        num2 = random.randint(1, 99)
        operation = random.choice(["+", "-", "*"])

        if operation == "+":
            return f"{num1} + {num2}", num1 + num2
        elif operation == "-":
            return f"{num1} - {num2}", num1 - num2
        elif operation == "*":
            return f"{num1} * {num2}", num1 * num2

    def open_settings(self):
        if self.check_math_problems():
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

        buttons_layout = QHBoxLayout()

        ok_button = QPushButton("OK")
        ok_button.setObjectName("dialogButton")
        ok_button.clicked.connect(lambda: self.save_settings(dialog, math_problems_input.text(), redirect_ip_input.text()))
        buttons_layout.addWidget(ok_button)

        restore_default_button = QPushButton(self.language["restore_default"])
        restore_default_button.setObjectName("dialogButton")
        restore_default_button.clicked.connect(lambda: redirect_ip_input.setText(default_redirect_ip))
        buttons_layout.addWidget(restore_default_button)

        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)

        dialog.exec_()

    def save_settings(self, dialog, math_problems, redirect_ip):
        try:
            self.settings["math_problems"] = int(math_problems)
        except ValueError:
            self.settings["math_problems"] = 0
        self.settings["redirect_ip"] = redirect_ip.strip() or default_redirect_ip
        self.settings["language"] = self.language_combo.currentText()
        dialog.accept()
        self.update_language()

    def update_language(self):
        self.language = languages[self.settings["language"]]
        self.setWindowTitle(self.language["title"])
        self.block_button.setText(self.language["block_websites"] if not self.check_websites_blocked() else self.language["unblock_websites"])
        self.settings_button.setText(self.language["settings"])
        self.manage_websites_button.setText(self.language["manage_websites"])

    def update_buttons(self):
        if self.check_websites_blocked():
            self.block_button.setText(self.language["unblock_websites"])
            self.block_button.setStyleSheet("background-color: #28a745; color: white;")
        else:
            self.block_button.setText(self.language["block_websites"])
            self.block_button.setStyleSheet("background-color: #ff6666; color: white;")

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

        website_input = QLineEdit()
        website_input.setPlaceholderText(self.language["no_website_entered"])
        layout.addWidget(website_input)

        buttons_layout = QHBoxLayout()

        add_button = QPushButton(self.language["add"])
        add_button.setObjectName("dialogButton")
        add_button.clicked.connect(lambda: self.add_website(website_input.text()))
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
        blocked_websites = self.load_blocked_websites()
        self.website_list.addItems(blocked_websites)

    def add_website(self, website):
        if website:
            blocked_websites = self.load_blocked_websites()
            blocked_websites.append(website)
            self.save_blocked_websites(blocked_websites)
            self.update_website_list()

    def remove_selected_website(self):
        selected_item = self.website_list.currentItem()
        if selected_item:
            website = selected_item.text()
            blocked_websites = self.load_blocked_websites()
            blocked_websites.remove(website)
            self.save_blocked_websites(blocked_websites)
            self.update_website_list()

    def restore_from_hosts(self):
        try:
            with open(hosts_path, 'r') as file:
                lines = file.readlines()
            blocked_websites = self.load_blocked_websites()
            for line in lines:
                if line.startswith(self.settings["redirect_ip"]):
                    website = line.split()[1]
                    if website not in blocked_websites:
                        blocked_websites.append(website)
            self.save_blocked_websites(blocked_websites)
            self.update_website_list()
        except Exception as e:
            QMessageBox.critical(self, self.language["error"], str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = App()
    main_app.run_as_admin()
    main_app.show()
    sys.exit(app.exec_())
