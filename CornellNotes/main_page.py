from ui_main_page import Ui_MainPage
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from note_page import NotePage

class MainPage(QMainWindow, Ui_MainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()
    def connect(self):
        # File Menu初始化
        self.actionNewProgram_2.triggered.connect(self.new_program)
        self.actionNewNote_2.triggered.connect(self.new_note)
        self.actionOpen_2.triggered.connect(self.open)
        self.actionSave_2.triggered.connect(self.save)
        self.actionSaveAs_2.triggered.connect(self.save_as)
        # 功能初始化
        self.searchButton.clicked.connect(self.search)

    def search(self):
        pass

    def new_program(self):
        pass

    def new_note(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())