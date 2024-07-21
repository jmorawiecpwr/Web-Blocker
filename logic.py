import os
import random
from settings import hosts_path, blocked_websites_file, default_redirect_ip, languages
from PyQt5.QtWidgets import QInputDialog, QMessageBox

class Logic:
    def __init__(self, settings):
        self.settings = settings

    def modify_hosts_file(self, block=True):
        try:
            with open(hosts_path, 'r+') as file:
                content = file.read()
                websites_to_block = self.load_blocked_websites()
                if block:
                    if not websites_to_block:
                        QMessageBox.critical(None, languages[self.settings["language"]]["error"], languages[self.settings["language"]]["blocking_list_empty"])
                        return
                    for website in websites_to_block:
                        if website not in content:
                            file.write(f"{self.settings['redirect_ip']} {website}\n")
                else:
                    file.seek(0)
                    new_content = [line for line in content.splitlines() if not any(website in line for website in websites_to_block)]
                    file.truncate(0)
                    file.write("\n".join(new_content))
        except PermissionError:
            QMessageBox.critical(None, languages[self.settings["language"]]["error"], "Permission denied to modify hosts file. Run the script as an administrator.")
        except FileNotFoundError:
            QMessageBox.critical(None, languages[self.settings["language"]]["error"], f"Hosts file not found: {hosts_path}")
        except Exception as e:
            QMessageBox.critical(None, languages[self.settings["language"]]["error"], f"Failed to modify hosts file: {e}")

    def load_blocked_websites(self):
        if os.path.exists(blocked_websites_file):
            with open(blocked_websites_file, 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    def save_blocked_websites(self, websites):
        with open(blocked_websites_file, 'w') as file:
            for website in websites:
                file.write(f"{website}\n")

    def remove_websites_containing(self, pattern):
        blocked_websites = self.load_blocked_websites()
        blocked_websites = [website for website in blocked_websites if pattern not in website]
        self.save_blocked_websites(blocked_websites)

        try:
            with open(hosts_path, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                file.truncate()
                file.writelines(line for line in lines if pattern not in line)
        except Exception as e:
            QMessageBox.critical(None, languages[self.settings["language"]]["error"], f"Error while modifying hosts file: {e}")

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
            user_answer, ok = QInputDialog.getInt(None, languages[self.settings["language"]]["math_problem"],
                                                  f"{languages[self.settings['language']]['solve']} {question}")
            if ok and user_answer == answer:
                correct_answers += 1
            else:
                QMessageBox.critical(None, languages[self.settings["language"]]["error"],
                                     languages[self.settings["language"]]["wrong_answer"])
                return False

        if correct_answers == problems_needed:
            return True
        else:
            QMessageBox.critical(None, languages[self.settings["language"]]["error"],
                                 languages[self.settings["language"]]["not_enough_correct"])
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