from ui_main_page import Ui_MainPage
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import os
from note_page import NotePage

class MainPage(QMainWindow, Ui_MainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()
        self.load_memo_content()
    def connect(self):
        # File Menu初始化
        self.actionNewProgram_2.triggered.connect(self.new_program)
        self.actionNewNote_2.triggered.connect(self.new_note)
        self.actionOpen_2.triggered.connect(self.open)
        self.actionSave_2.triggered.connect(self.save)
        self.actionSaveAs_2.triggered.connect(self.save_as)
        # 功能初始化
        self.searchButton.clicked.connect(self.search)

    def load_memo_content(self):
        memo_folder = os.path.join('resources', 'memo')
        memo_content = ''
        if os.path.exists(memo_folder) and os.path.isdir(memo_folder):
            for filename in os.listdir(memo_folder):
                file_path = os.path.join(memo_folder, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        memo_content += file.read() + '\n'
        self.toDo.setPlainText(memo_content)

    def save_memo_content(self):
        memo_folder = os.path.join('resources', 'memo')
        if not os.path.exists(memo_folder):
            os.makedirs(memo_folder)
        memo_file_path = os.path.join(memo_folder, 'memo.note')
        with open(memo_file_path, 'w') as file:
            file.write(self.toDo.toPlainText())

    def closeEvent(self, event):
        # print("Closing event triggered, saving memo content.")
        # print("toDo content:", self.toDo.toPlainText())
        self.save_memo_content()
        event.accept()

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