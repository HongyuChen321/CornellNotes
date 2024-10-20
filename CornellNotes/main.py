import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from note_page import NotePage
from main_page import MainPage

class MainWindow(QMainWindow, MainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())