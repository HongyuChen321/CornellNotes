from ui_note_page import Ui_CornellNotes
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTextEdit, QAction, QFontDialog, QColorDialog
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QTextCursor, QImage
import sys
import os
from unittest import findTestCases

class NotePage(QMainWindow, Ui_CornellNotes):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()
        self.saved = False  # 初始状态为未保存
        self.current_filename = None  # 初始没有当前文件名
        self.last_open_directory = os.getcwd()  # 上次打开的目录
        self.new_folder_path = None  # 新建的文件夹路径，初始为空
        self.current_text_edit = None

        # 设置默认字体大小
        self.set_default_font_size(11)

        # 连接聚焦事件
        self.MainNotes.installEventFilter(self)
        self.keyWords.installEventFilter(self)
        self.conclusion.installEventFilter(self)

    def connect(self):
        # File Menu初始化
        self.actionNewProgram.triggered.connect(self.new_program)
        self.actionNewNote.triggered.connect(self.new_note)
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionSaveAs.triggered.connect(self.save_as)
        # 功能初始化
        self.fontSet.clicked.connect(self.font_set)
        self.Bold.clicked.connect(self.bold)
        self.Italic.clicked.connect(self.italic)
        self.Underline.clicked.connect(self.underline)
        self.Left.clicked.connect(self.left)
        self.Right.clicked.connect(self.right)
        self.Center.clicked.connect(self.center)
        self.LeftAndRight.clicked.connect(self.left_and_right)
        self.Superscript.clicked.connect(self.superscript)
        self.Subscript.clicked.connect(self.subscript)
        self.InsertPicture.clicked.connect(self.insert_picture)
        self.FontColour.clicked.connect(self.font_colour)


    def set_default_font_size(self, size):
        font = self.MainNotes.font()
        font.setPointSize(size)
        self.MainNotes.setFont(font)
        self.keyWords.setFont(font)
        self.conclusion.setFont(font)

    def new_program(self):
        folder_name, ok = QInputDialog.getText(self, "Create New Folder", "Enter folder name:")
        if not ok or not folder_name:
            return

        base_dir = os.getcwd()
        self.new_folder_path = os.path.join(base_dir, folder_name)  # 存储新创建的文件夹路径

        try:
            os.makedirs(self.new_folder_path, exist_ok=True)
            QMessageBox.information(self, "Success", f"Folder '{folder_name}' created successfully.")

            default_note_path = os.path.join(self.new_folder_path, "default_note.note")
            try:
                with open(default_note_path, 'w') as file:
                    file.write("This is a default note.")
                QMessageBox.information(self, "Success", f"Default note '{default_note_path}' created successfully.")
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Failed to create default note in folder '{folder_name}': {e}")

        except OSError as e:
            QMessageBox.critical(self, "Error", f"Failed to create folder '{folder_name}': {e}")
            del self.new_folder_path

    def new_note(self):
        self.MainNotes.clear()
        self.keyWords.clear()
        self.conclusion.clear()
        self.saved = False
        self.current_filename = None  # 重置当前文件名
        QMessageBox.information(self, "Note Cleared", "The note interface has been cleared.")

    def open(self):
        start_dir = getattr(self, 'new_folder_path', self.last_open_directory)
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", start_dir, "Note Files (*.note)")
        if filename:
            with open(filename, 'r') as file:
                content = file.read().split('###\n', 2)
                if len(content) == 3:
                    keywords, mainNotes, conclusion = content
                    self.keyWords.setPlainText(keywords)
                    self.MainNotes.setPlainText(mainNotes)
                    self.conclusion.setPlainText(conclusion)
                    self.saved = True
                    self.current_filename = filename
                    self.last_open_directory = os.path.dirname(filename)  # 更新上次打开的目录

    def save(self):
        if self.current_filename:  # 如果已经打开了文件，则直接保存
            with open(self.current_filename, 'w') as file:
                textKeywords = self.keyWords.toPlainText()
                textMainNotes = self.MainNotes.toPlainText()
                textConclusion = self.conclusion.toPlainText()
                file.write(textKeywords + '###\n' + textMainNotes + '###\n' + textConclusion)
            self.saved = True  # 更新保存状态
        else:  # 如果没有打开文件（即新建的笔记），则调用 save_as 方法
            self.save_as()

    def save_as(self):
        start_dir = getattr(self, 'new_folder_path', self.last_open_directory)

        filename, _ = QFileDialog.getSaveFileName(self, "Save File", start_dir, "Note Files (*.note)")
        if filename:
            with open(filename, 'w') as file:
                textKeywords = self.keyWords.toPlainText()
                textMainNotes = self.MainNotes.toPlainText()
                textConclusion = self.conclusion.toPlainText()
                file.write(textKeywords + '###\n' + textMainNotes + '###\n' + textConclusion)
            self.saved = True
            self.current_filename = filename
            self.last_open_directory = os.path.dirname(filename)  # 更新上次打开的目录

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj in [self.MainNotes, self.keyWords, self.conclusion]:
                self.current_text_edit = obj
        return super().eventFilter(obj, event)


    def bold(self):
        if self.current_text_edit:
            cursor = self.current_text_edit.textCursor()
            if cursor.hasSelection():
                fmt = cursor.charFormat()
                weight = QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal
                fmt.setFontWeight(weight)
                cursor.mergeCharFormat(fmt)
                self.current_text_edit.mergeCurrentCharFormat(fmt)

    def italic(self):
        if self.current_text_edit:
            cursor = self.current_text_edit.textCursor()
            if cursor.hasSelection():
                fmt = cursor.charFormat()
                fmt.setFontItalic(not fmt.fontItalic())
                cursor.mergeCharFormat(fmt)
                self.current_text_edit.mergeCurrentCharFormat(fmt)

    def underline(self):
        if self.current_text_edit:
            cursor = self.current_text_edit.textCursor()
            if cursor.hasSelection():
                fmt = cursor.charFormat()
                fmt.setFontUnderline(not fmt.fontUnderline())
                cursor.mergeCharFormat(fmt)
                self.current_text_edit.mergeCurrentCharFormat(fmt)

    def font_colour(self):
        if self.current_text_edit:
            colour = QColorDialog.getColor(self.current_text_edit.textColor(), self)
            if colour.isValid():
                cursor = self.current_text_edit.textCursor()
                if cursor.hasSelection():
                    fmt = cursor.charFormat()
                    fmt.setForeground(colour)
                    cursor.mergeCharFormat(fmt)
                    self.current_text_edit.mergeCurrentCharFormat(fmt)

    def left(self):
        pass

    def right(self):
        pass

    def center(self):
        pass

    def left_and_right(self):
        pass

    def superscript(self):
        # 切换选中文本的上标状态
        cursor = self.MainNotes.textCursor()
        current_format = cursor.charFormat()
        format = QTextCharFormat()
        if current_format.verticalAlignment() == QTextCharFormat.AlignSuperScript:
            format.setVerticalAlignment(QTextCharFormat.AlignNormal)
        else:
            format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
        self.apply_text_format(format)

    def subscript(self):
        # 切换选中文本的下标状态
        cursor = self.MainNotes.textCursor()
        current_format = cursor.charFormat()
        format = QTextCharFormat()
        if current_format.verticalAlignment() == QTextCharFormat.AlignSubScript:
            format.setVerticalAlignment(QTextCharFormat.AlignNormal)
        else:
            format.setVerticalAlignment(QTextCharFormat.AlignSubScript)
        self.apply_text_format(format)

    def insert_picture(self):
        # 插入可调整大小的图片
        filename, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if filename:
            image = QImage(filename)
            if not image.isNull():
                factor, ok = QInputDialog.getDouble(self, "Insert Image", "Enter scale factor (e.g., 1.0, 0.5, etc.):",
                                                    1.0, 0.1, 10.0, 1)
                if ok:
                    image = image.scaled(image.width() * factor, image.height() * factor, Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
                    cursor = self.MainNotes.textCursor()
                    cursor.insertImage(image)

    def apply_text_format(self, format):
        # 应用文本格式
        cursor = self.MainNotes.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.MainNotes.mergeCurrentCharFormat(format)

    def font_set(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotePage()
    window.show()
    sys.exit(app.exec_())