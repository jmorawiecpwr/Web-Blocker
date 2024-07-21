import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/app.ico"))
    main_app = App()
    main_app.run_as_admin()
    main_app.show()
    sys.exit(app.exec_())