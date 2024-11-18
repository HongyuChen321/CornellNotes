import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from note_page import NotePage
from main_page import MainPage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())