from ui_main_page import Ui_MainPage
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QInputDialog
import sys
import os
from note_page import NotePage

class MainPage(QMainWindow, Ui_MainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()
        self.load_memo_content()
        self.note_page = NotePage()
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
                    with open(file_path, 'r', encoding='UTF-8') as file:
                        memo_content += file.read() + '\n'
        self.toDo.setPlainText(memo_content)

    def save_memo_content(self):
        memo_folder = os.path.join('resources', 'memo')
        if not os.path.exists(memo_folder):
            os.makedirs(memo_folder)
        memo_file_path = os.path.join(memo_folder, 'memo.note')
        with open(memo_file_path, 'w', encoding='UTF-8') as file:
            file.write(self.toDo.toPlainText())

    def closeEvent(self, event):
        # print("Closing event triggered, saving memo content.")
        # print("toDo content:", self.toDo.toPlainText())
        self.save_memo_content()
        event.accept()

    def search(self):
        keyword = self.searchBar.toPlainText().strip()
        if not keyword:
            print("No keyword entered.")  # 调试输出
            return  # 如果没有输入关键词，则返回

        # 指定笔记文件存储路径
        notes_directory = QFileDialog.getExistingDirectory(self, "选择文件夹")
        print(notes_directory)

        # notes_directory = "folder_path" # 替换为实际路径
        matching_files = []  # 用于存储匹配的文件名

        for root, dirs, files in os.walk(notes_directory):
            for filename in files:
                if filename.endswith(".note"):
                    file_path = os.path.join(root, filename)
                    print(filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # 检查文件内容是否包含关键词
                        if keyword in content:
                            matching_files.append(file_path)  # 添加匹配的文件名

            print(matching_files)  # 显示调试

        # 显示
        if not matching_files:
            QMessageBox.information(None, "提示", "没有匹配到相关文件哦。")
            return

        file_content = "\n".join(matching_files)
        msg_box = QMessageBox()
        msg_box.setWindowTitle("检索结果")
        msg_box.setText(file_content)
        msg_box.exec_()

    def new_program(self):
        folder_name, ok = QInputDialog.getText(self, "Create New Folder", "Enter folder name:")
        if not ok or not folder_name:
            return

        base_dir = "notes"
        self.new_folder_path = os.path.join(base_dir, folder_name)  # 存储新创建的文件夹路径

        try:
            os.makedirs(self.new_folder_path, exist_ok=True)
            QMessageBox.information(self, "Success", f"Folder '{folder_name}' created successfully.")

        except OSError as e:
            QMessageBox.critical(self, "Error", f"Failed to create folder '{folder_name}': {e}")
            self.new_folder_path = None  # 如果失败则将文件夹路径置为空

    def new_note(self):
        if self.note_page.isHidden():
            self.note_page.show()
        else:
            self.note_page.new_note()

    def open(self):
        if self.note_page.isHidden():
            self.note_page.show()
            self.note_page.open()
        else:
            self.note_page.open()

    def save(self):
        pass

    def save_as(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())