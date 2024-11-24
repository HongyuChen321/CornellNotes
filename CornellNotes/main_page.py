from ui_main_page import Ui_MainPage
from note_page import NotePage
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QInputDialog, QDialog, QTextBrowser, QVBoxLayout, QShortcut
from PyQt5.QtGui import QKeySequence, QKeyEvent
from PyQt5.QtCore import QDir, Qt, QStringListModel
import sys, os
from urllib.parse import unquote


class MainPage(QMainWindow, Ui_MainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()  # 连接信号与槽
        self.model = QStringListModel() # 创建QStringListModel
        self.noteMenu.setModel(self.model)  # 将model设置到noteMenu
        self.note_page = NotePage() # 创建NotePage实例
        self.auto_list_files()  # 自动列出文件
        self.last_dubble_clicked_path = 'notes' # 存储上次双击的文件夹路径
        self.add_shortcuts()    # 添加快捷键
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)  # 禁用最大化按钮
        self.load_memo_content()    # 读取备忘录内容
        self.searchBar.installEventFilter(self) # 安装事件过滤器
        self.connect_scrollbar()    # 关联滚动条与文本框

    def eventFilter(self, obj, event):
        if obj == self.searchBar and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # print("回车键被按下，触发自定义行为")
                self.handle_enter_key()
                return True  # 阻止默认行为
        return super().eventFilter(obj, event)

    def connect(self):
        # File Menu初始化
        self.actionNewProgram_2.triggered.connect(self.new_program)
        self.actionNewNote_2.triggered.connect(self.new_note)
        self.actionOpen_2.triggered.connect(self.open)
        self.actionSave_2.triggered.connect(self.save)
        self.actionSaveAs_2.triggered.connect(self.save_as)
        # 功能初始化
        self.searchButton.clicked.connect(self.search)
        self.listButton.clicked.connect(self.list_files)
        self.noteMenu.doubleClicked.connect(self.on_noteMenu_double_clicked)

    def handle_enter_key(self):
        keyword = self.searchBar.toPlainText().strip()
        if not keyword:
            print("No keyword entered.")  # 调试输出
            return  # 如果没有输入关键词，则返回

        # 指定笔记文件存储路径
        notes_directory = 'notes'
        matching_files = []  # 用于存储匹配的文件路径

        for root, dirs, files in os.walk(notes_directory):
            for filename in files:
                if filename.endswith(".note"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if keyword in content:
                            matching_files.append(file_path)

        print(f"Matching files: {matching_files}")  # 显示调试

        # 显示
        if not matching_files:
            QMessageBox.information(None, "提示", "没有匹配到相关文件哦。")
            return

        self.display_results(matching_files)

    # 关联滚动条与文本框
    def connect_scrollbar(self):
        self.verticalScrollBarToDo.valueChanged.connect(self.toDo.verticalScrollBar().setValue)
        self.toDo.verticalScrollBar().valueChanged.connect(self.verticalScrollBarToDo.setValue)

        self.verticalScrollBarNoteMenu.valueChanged.connect(self.noteMenu.verticalScrollBar().setValue)
        self.noteMenu.verticalScrollBar().valueChanged.connect(self.verticalScrollBarNoteMenu.setValue)

    # 添加快捷键
    def add_shortcuts(self):
        # 添加新建笔记快捷键 Ctrl+N
        new_note_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_note_shortcut.activated.connect(self.new_note)

    # 自动列出文件
    def auto_list_files(self):
        # 指定要自动列出文件的目录
        directory = 'notes'
        if directory:
            # 清除旧的文件列表
            self.model.setStringList([])

            # 使用QDir遍历目录中的文件
            dir_obj = QDir(directory)
            file_list = dir_obj.entryList(['*'], QDir.Files | QDir.Dirs | QDir.NoDotAndDotDot)

            # 将文件列表转换为QStringList，并设置到模型中
            self.model.setStringList(list(file_list))

    # 双击文件夹或文件打开文件夹或文件
    def on_noteMenu_double_clicked(self, index):
        # 获取双击的文件路径
        file_path = self.model.stringList()[index.row()]
        full_file_path = os.path.join(self.last_dubble_clicked_path, file_path)
        if os.path.isdir(full_file_path):
            self.last_dubble_clicked_path = full_file_path
        print(f"Double clicked: {full_file_path}")

        if os.path.isdir(full_file_path):
            # 如果是文件夹，清空viewlist并显示此文件夹中的所有文件名
            self.model.setStringList([])
            dir_obj = QDir(full_file_path)
            file_list = dir_obj.entryList(['*'], QDir.Files | QDir.Dirs | QDir.NoDotAndDotDot)
            self.model.setStringList(list(file_list))
            self.last_dubble_clicked_path = full_file_path
        elif os.path.isfile(full_file_path) and full_file_path.endswith('.note'):
            # 如果是note文件
            if not self.note_page.isHidden():
                # 如果NotePage已打开，自动保存内容并清除内容
                self.note_page.save()
                self.note_page.keyWords.clear()
                self.note_page.MainNotes.clear()
                self.note_page.conclusion.clear()
            else:
                # 如果NotePage未打开，则打开NotePage
                self.note_page.show()

            # 显示双击note文件内的内容
            try:
                with open(full_file_path, 'r', encoding="UTF-8") as file:
                    content = file.read()
                    parts = content.split('\n###\n', 2)
                    if len(parts) != 3:
                        raise ValueError("File format error: Missing sections.")
                    keywords, mainNotes, conclusion = parts
                    self.note_page.keyWords.setHtml(keywords)
                    self.note_page.MainNotes.setHtml(mainNotes)
                    self.note_page.conclusion.setHtml(conclusion)
                    self.note_page.saved = False
                    self.note_page.current_filename = full_file_path  # 存储完整路径
                    self.note_page.last_open_directory = os.path.dirname(full_file_path)  # 更新上次打开的目录
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", f"File not found: {full_file_path}")
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Error", f"Failed to decode file: {full_file_path}")
            except ValueError as ve:
                QMessageBox.critical(self, "Error", str(ve))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

    # 列出文件
    def list_files(self):
        #         # 打开目录选择对话框
        directory = 'notes'
        self.last_dubble_clicked_path = directory

        if directory:
            # 清除旧的文件列表
            self.model.setStringList([])

            # 使用QDir遍历目录中的文件
            dir_obj = QDir(directory)
            file_list = dir_obj.entryList(['*'], QDir.Files | QDir.Dirs | QDir.NoDotAndDotDot)

            # 将文件列表转换为QStringList，并设置到模型中
            self.model.setStringList(list(file_list))
            self.last_dubble_clicked_path = directory

    # 读取备忘录内容
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

    # 保存备忘录内容
    def save_memo_content(self):
        memo_folder = os.path.join('resources', 'memo')
        if not os.path.exists(memo_folder):
            os.makedirs(memo_folder)
        memo_file_path = os.path.join(memo_folder, 'memo.note')
        with open(memo_file_path, 'w', encoding='UTF-8') as file:
            file.write(self.toDo.toPlainText())

    # 关闭窗口时保存备忘录内容
    def closeEvent(self, event):
        self.save_memo_content()
        event.accept()

    # 搜索
    def search(self):
        keyword = self.searchBar.toPlainText().strip()
        if not keyword:
            print("No keyword entered.")  # 调试输出
            return  # 如果没有输入关键词，则返回

        # 指定笔记文件存储路径
        absolute_path = QFileDialog.getExistingDirectory(self, "选择检索文件夹", "notes")
        notes_directory = os.path.relpath(absolute_path)
        matching_files = []  # 用于存储匹配的文件路径

        for root, dirs, files in os.walk(notes_directory):
            for filename in files:
                if filename.endswith(".note"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if keyword in content:
                            matching_files.append(file_path)

        print(f"Matching files: {matching_files}")  # 显示调试

        # 显示
        if not matching_files:
            QMessageBox.information(None, "提示", "没有匹配到相关文件哦。")
            return

        self.display_results(matching_files)

    # 显示检索结果
    def display_results(self, matching_files):
        dialog = QDialog(self)
        dialog.setWindowTitle("检索结果")
        dialog.resize(400, 300)

        text_browser = QTextBrowser(dialog)
        html_content = "<p>找到以下匹配文件：</p><ul>"
        for file_path in matching_files:
            # 标准化路径并替换反斜杠为正斜杠
            norm_file_path = os.path.normpath(file_path).replace('\\', '/')
            encoded_file_path = norm_file_path
            # 使用 os.path.basename(file_path) 提取文件名作为链接文本
            link_text = f"<a href='file://{encoded_file_path}'>{file_path}</a><br/>"
            html_content += f"<li>{link_text}</li>"
        html_content += "</ul>"

        text_browser.setHtml(html_content)
        text_browser.setOpenExternalLinks(False)
        text_browser.anchorClicked.connect(lambda url: self.open_file(url, dialog))

        layout = QVBoxLayout()
        layout.addWidget(text_browser)
        dialog.setLayout(layout)

        dialog.exec_()

    # 打开文件
    def open_file(self, url, parent_dialog):
        full_file_path = unquote(url.toString()).replace('file://', '')
        full_file_path = full_file_path.replace('\\', '/')
        if len(full_file_path) > 1 and full_file_path[0].lower() == 'c' and full_file_path[1] != ':':
            full_file_path = 'C:' + full_file_path[1:]  # 添加驱动器字母和冒号，并删除原来的第一个字符
        elif len(full_file_path) > 1 and full_file_path[0].lower() == 'd' and full_file_path[1] != ':':
            full_file_path = 'D:' + full_file_path[1:]  # 添加驱动器字母和冒号，并删除原来的第一个字符
        elif len(full_file_path) > 1 and full_file_path[0].lower() == 'e' and full_file_path[1] != ':':
            full_file_path = 'E:' + full_file_path[1:]  # 添加驱动器字母和冒号，并删除原来的第一个字符
        elif len(full_file_path) > 1 and full_file_path[0].lower() == 'f' and full_file_path[1] != ':':
            full_file_path = 'F:' + full_file_path[1:]  # 添加驱动器字母和冒号，并删除原来的第一个字符
        elif len(full_file_path) > 0 and full_file_path[0].lower() == 'c':
            full_file_path = 'C:' + full_file_path[1:]  # 添加驱动器字母和冒号
        elif len(full_file_path) > 0 and full_file_path[0].lower() == 'd':
            full_file_path = 'D:' + full_file_path[1:]  # 添加驱动器字母和冒号
        elif len(full_file_path) > 0 and full_file_path[0].lower() == 'e':
            full_file_path = 'E:' + full_file_path[1:]  # 添加驱动器字母和冒号
        elif len(full_file_path) > 0 and full_file_path[0].lower() == 'f':
            full_file_path = 'F:' + full_file_path[1:]  # 添加驱动器字母和冒号
        print(f"Opening file: {full_file_path}")

        if not full_file_path or not os.path.exists(full_file_path):
            QMessageBox.critical(self, "Error", "Invalid file path or file does not exist.")
            return

        filename = os.path.basename(full_file_path)  # 提取文件名

        if self.note_page.isHidden():
            self.note_page.show()
            self.note_page.raise_()
            self.note_page.activateWindow()
            if filename:
                try:
                    with open(full_file_path, 'r', encoding="UTF-8") as file:
                        content = file.read()
                        parts = content.split('\n###\n', 2)
                        if len(parts) != 3:
                            raise ValueError("File format error: Missing sections.")
                        keywords, mainNotes, conclusion = parts
                        self.note_page.keyWords.setHtml(keywords)
                        self.note_page.MainNotes.setHtml(mainNotes)
                        self.note_page.conclusion.setHtml(conclusion)
                        self.note_page.saved = False
                        self.note_page.current_filename = full_file_path  # 存储完整路径
                        self.note_page.last_open_directory = os.path.dirname(full_file_path)  # 更新上次打开的目录
                        self.note_page.show()  # 显示笔记页面
                except FileNotFoundError:
                    QMessageBox.critical(self, "Error", f"File not found: {full_file_path}")
                except UnicodeDecodeError:
                    QMessageBox.critical(self, "Error", f"Failed to decode file: {full_file_path}")
                except ValueError as ve:
                    QMessageBox.critical(self, "Error", str(ve))
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

            parent_dialog.close()  # 关闭检索结果对话框

        else:
            if filename:
                try:
                    with open(full_file_path, 'r', encoding="UTF-8") as file:
                        content = file.read()
                        parts = content.split('\n###\n', 2)
                        if len(parts) != 3:
                            raise ValueError("File format error: Missing sections.")
                        keywords, mainNotes, conclusion = parts
                        self.note_page.keyWords.setHtml(keywords)
                        self.note_page.MainNotes.setHtml(mainNotes)
                        self.note_page.conclusion.setHtml(conclusion)
                        self.note_page.saved = False
                        self.note_page.current_filename = full_file_path  # 存储完整路径
                        self.note_page.last_open_directory = os.path.dirname(full_file_path)  # 更新上次打开的目录
                        self.note_page.show()  # 显示笔记页面
                        self.note_page.raise_()
                        self.note_page.activateWindow()
                except FileNotFoundError:
                    QMessageBox.critical(self, "Error", f"File not found: {full_file_path}")
                except UnicodeDecodeError:
                    QMessageBox.critical(self, "Error", f"Failed to decode file: {full_file_path}")
                except ValueError as ve:
                    QMessageBox.critical(self, "Error", str(ve))
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

            parent_dialog.close()  # 关闭检索结果对话框

    # 创建新的文件夹
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

    # 创建新的笔记
    def new_note(self):
        if self.note_page.isHidden():
            self.note_page.show()
        else:
            self.note_page.new_note()

    # 打开笔记
    def open(self):
        if self.note_page.isHidden():
            self.note_page.show()
            self.note_page.open()
        else:
            self.note_page.open()

    # 保存笔记
    def save(self):
        pass

    # 另存为
    def save_as(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())