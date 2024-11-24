from ui_note_page import Ui_CornellNotes
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTextEdit, QAction, QFontDialog, QColorDialog, QMessageBox, QInputDialog, QShortcut
from PyQt5.QtCore import Qt, QEvent, QBuffer
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QTextCursor, QImage, QKeySequence
import sys
import os
from unittest import findTestCases
import base64
from io import BytesIO

class NotePage(QMainWindow, Ui_CornellNotes):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()  # 连接信号和槽
        self.saved = False  # 初始状态为未保存
        self.current_filename = None  # 初始没有当前文件名
        self.new_folder_path = None  # 新建的文件夹路径，初始为空
        self.current_text_edit = None   # 当前文本编辑框
        self.last_open_directory = os.getcwd()  # 上次打开的目录
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)  # 禁止最大化
        self.add_shortcuts()     # 快捷键
        self.set_default_font_size(11)  # 设置默认字体大小
        self.buttonDisplay()    # 按钮显示
        self.connect_scrollbar()  # 关联滚动条和文本框

        # 连接聚焦事件
        self.MainNotes.installEventFilter(self)
        self.keyWords.installEventFilter(self)
        self.conclusion.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj in [self.MainNotes, self.keyWords, self.conclusion]:
                self.current_text_edit = obj
        return super().eventFilter(obj, event)

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

    # 关联滚动条和文本框
    def connect_scrollbar(self):
        self.verticalScrollBarKeywords.valueChanged.connect(self.keyWords.verticalScrollBar().setValue)
        self.keyWords.verticalScrollBar().valueChanged.connect(self.verticalScrollBarKeywords.setValue)

        self.verticalScrollBarMainNotes.valueChanged.connect(self.MainNotes.verticalScrollBar().setValue)
        self.MainNotes.verticalScrollBar().valueChanged.connect(self.verticalScrollBarMainNotes.setValue)

        self.verticalScrollBarConclusion.valueChanged.connect(self.conclusion.verticalScrollBar().setValue)
        self.conclusion.verticalScrollBar().valueChanged.connect(self.verticalScrollBarConclusion.setValue)

    # 按钮显示
    def buttonDisplay(self):
        self.fontSet.setToolTip("字体设置")
        self.Bold.setToolTip("加粗")
        self.Italic.setToolTip("斜体")
        self.Underline.setToolTip("下划线")
        self.Left.setToolTip("左对齐")
        self.Right.setToolTip("右对齐")
        self.Center.setToolTip("居中")
        self.LeftAndRight.setToolTip("两端对齐")
        self.Superscript.setToolTip("上标")
        self.Subscript.setToolTip("下标")
        self.InsertPicture.setToolTip("插入图片")
        self.FontColour.setToolTip("字体颜色")

    # 添加快捷键
    def add_shortcuts(self):
        # 添加保存快捷键 Ctrl+S
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save)

        # 添加新建笔记快捷键 Ctrl+N
        new_note_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_note_shortcut.activated.connect(self.new_note)

        # 加粗快捷键 Ctrl+B
        bold_shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        bold_shortcut.activated.connect(self.bold)

        # 斜体快捷键 Ctrl+I
        italic_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        italic_shortcut.activated.connect(self.italic)

        # 下划线快捷键 Ctrl+U
        underline_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        underline_shortcut.activated.connect(self.underline)

    # 设置默认字体大小
    def set_default_font_size(self, size):
        font = self.MainNotes.font()
        font.setPointSize(size)
        self.MainNotes.setFont(font)
        self.keyWords.setFont(font)
        self.conclusion.setFont(font)

    # 新建文件夹
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

    # 新建笔记
    def new_note(self):
        if self.saved == True:
            self.MainNotes.clear()
            self.keyWords.clear()
            self.conclusion.clear()
            self.saved = False
            self.current_filename = None  # 重置当前文件名
            QMessageBox.information(self, "Note Cleared", "The note interface has been cleared.")
        elif self.saved == False:
            reply = QMessageBox.question(self, "Save Changes", "Do you want to save the changes?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save()
                self.MainNotes.clear()
                self.keyWords.clear()
                self.conclusion.clear()
                self.saved = False
                self.current_filename = None

    # 打开文件
    def open(self):
        # 如果当前笔记为空，则直接打开文件
        if (self.keyWords.toPlainText() == "" and self.MainNotes.toPlainText() == "" and self.conclusion.toPlainText() == "") or self.saved == True :
            start_dir = 'notes'
            filename, _ = QFileDialog.getOpenFileName(self, "Open File", start_dir, "Note Files (*.note)")
            if filename:
                try:
                    with open(filename, 'r', encoding = "UTF-8") as file:
                        keywords, mainNotes, conclusion = file.read().split('\n###\n', 2)
                        self.keyWords.setHtml(keywords)  # 使用 setPlainText 来加载纯文本内容
                        self.MainNotes.setHtml(mainNotes)
                        self.conclusion.setHtml(conclusion)
                        self.saved = False
                        self.current_filename = filename
                        self.last_open_directory = os.path.dirname(filename)  # 更新上次打开的目录
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open file: {e}")
        # 如果当前笔记不为空，则询问是否保存当前笔记
        elif self.saved == False:
            reply = QMessageBox.question(self, "Save Changes", "Do you want to save the changes?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save()
                self.saved = False
                self.current_filename = None
            self.MainNotes.clear()
            self.keyWords.clear()
            self.conclusion.clear()
            start_dir = 'notes'
            filename, _ = QFileDialog.getOpenFileName(self, "Open File", start_dir, "Note Files (*.note)")
            if filename:
                try:
                    with open(filename, 'r', encoding = "UTF-8") as file:
                        keywords, mainNotes, conclusion = file.read().split('\n###\n', 2)
                        self.keyWords.setHtml(keywords)  # 使用 setHtml 来加载 HTML 格式内容
                        self.MainNotes.setHtml(mainNotes)
                        self.conclusion.setHtml(conclusion)
                        self.saved = True
                        self.current_filename = filename
                        self.last_open_directory = os.path.dirname(filename)  # 更新上次打开的目录
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open file: {e}")

    # 保存文件
    def save(self):
        if self.current_filename:  # 如果已经打开了文件，则直接保存
            with open(self.current_filename, 'w', encoding = "UTF-8") as file:
                textKeywords = self.keyWords.toHtml()  # 使用HTML保存文本内容，包括格式和颜色
                textMainNotes = self.MainNotes.toHtml()
                textConclusion = self.conclusion.toHtml()
                file.write(textKeywords + '\n###\n' + textMainNotes + '\n###\n' + textConclusion)
            self.saved = True  # 更新保存状态
        else:  # 如果没有打开文件（即新建的笔记），则调用 save_as 方法
            self.save_as()

    # 另存为
    def save_as(self):
        start_dir = 'notes'
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", start_dir, "Note Files (*.note)")
        if filename:
            with open(filename, 'w', encoding = "UTF-8") as file:
                textKeywords = self.keyWords.toHtml()  # 使用HTML保存文本内容，包括格式和颜色
                textMainNotes = self.MainNotes.toHtml()
                textConclusion = self.conclusion.toHtml()
                file.write(textKeywords + '\n###\n' + textMainNotes + '\n###\n' + textConclusion)
            self.saved = True
            self.current_filename = filename
            self.last_open_directory = os.path.dirname(filename)  # 更新上次打开的目录

    # 加粗
    def bold(self):
        if self.current_text_edit:
            cursor = self.current_text_edit.textCursor()
            if cursor.hasSelection():
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                cursor.setPosition(start)

                while cursor.position() < end:
                    cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                    char_format = cursor.charFormat()
                    weight = QFont.Bold if char_format.fontWeight() != QFont.Bold else QFont.Normal
                    char_format.setFontWeight(weight)
                    cursor.mergeCharFormat(char_format)
                    cursor.clearSelection()

                cursor.setPosition(start, QTextCursor.MoveAnchor)
                self.current_text_edit.setTextCursor(cursor)

    # 斜体
    def italic(self):
        if self.current_text_edit:
            cursor = self.current_text_edit.textCursor()
            if cursor.hasSelection():
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                cursor.setPosition(start)

                while cursor.position() < end:
                    cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                    char_format = cursor.charFormat()
                    char_format.setFontItalic(not char_format.fontItalic())
                    cursor.mergeCharFormat(char_format)
                    cursor.clearSelection()

                cursor.setPosition(start, QTextCursor.MoveAnchor)
                self.current_text_edit.setTextCursor(cursor)

    # 下划线
    def underline(self):
        if self.current_text_edit:
            cursor = self.current_text_edit.textCursor()
            if cursor.hasSelection():
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                cursor.setPosition(start)

                while cursor.position() < end:
                    cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                    char_format = cursor.charFormat()
                    char_format.setFontUnderline(not char_format.fontUnderline())
                    cursor.mergeCharFormat(char_format)
                    cursor.clearSelection()

                cursor.setPosition(start, QTextCursor.MoveAnchor)
                self.current_text_edit.setTextCursor(cursor)

    # 字体颜色
    def font_colour(self):
        if self.current_text_edit:
            colour = QColorDialog.getColor(self.current_text_edit.textColor(), self)
            if colour.isValid():
                cursor = self.current_text_edit.textCursor()
                if cursor.hasSelection():
                    start = cursor.selectionStart()
                    end = cursor.selectionEnd()
                    cursor.setPosition(start)

                    while cursor.position() < end:
                        cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                        char_format = cursor.charFormat()
                        char_format.setForeground(colour)
                        cursor.mergeCharFormat(char_format)
                        cursor.clearSelection()

                    cursor.setPosition(start, QTextCursor.MoveAnchor)
                    self.current_text_edit.setTextCursor(cursor)

    # 左对齐
    def left(self):
        text_edits = [self.keyWords, self.MainNotes, self.conclusion]
        for text_edit in text_edits:
            cursor = text_edit.textCursor()
            if cursor.hasSelection():
                block_format = cursor.blockFormat()
                block_format.setAlignment(Qt.AlignLeft)
                cursor.setBlockFormat(block_format)

    # 右对齐
    def right(self):
        text_edits = [self.keyWords, self.MainNotes, self.conclusion]
        for text_edit in text_edits:
            cursor = text_edit.textCursor()
            if cursor.hasSelection():
                block_format = cursor.blockFormat()
                block_format.setAlignment(Qt.AlignRight)
                cursor.setBlockFormat(block_format)

    # 居中
    def center(self):
        text_edits = [self.keyWords, self.MainNotes, self.conclusion]
        for text_edit in text_edits:
            cursor = text_edit.textCursor()
            if cursor.hasSelection():
                block_format = cursor.blockFormat()
                block_format.setAlignment(Qt.AlignCenter)
                cursor.setBlockFormat(block_format)

    # 两端对齐
    def left_and_right(self):
        text_edits = [self.keyWords, self.MainNotes, self.conclusion]
        for text_edit in text_edits:
            cursor = text_edit.textCursor()
            if cursor.hasSelection():
                block_format = cursor.blockFormat()
                block_format.setAlignment(Qt.AlignJustify)
                cursor.setBlockFormat(block_format)

    # 上标
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

    # 下标
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

    # 插入图片
    def insert_picture(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)")
        if filename:
            image = QImage(filename)
            if not image.isNull():
                width, ok_width = QInputDialog.getInt(self, "Insert Image", "Enter width:", 100, 10, 1000)
                if ok_width:
                    height, ok_height = QInputDialog.getInt(self, "Insert Image", "Enter height:", 100, 10, 1000)
                    if ok_height:
                        new_width = width
                        new_height = height
                        image = image.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                        buffer = QBuffer()
                        buffer.open(QBuffer.ReadWrite)
                        image.save(buffer, "PNG")  # Ensure the specified file format is "PNG"
                        base64_data = base64.b64encode(buffer.data()).decode('utf-8')

                        html_img_tag = f'<img src="data:image/png;base64,{base64_data}" style="width:auto;height:auto;"/>'
                        if self.current_text_edit:  # Ensure there is a current text edit
                            cursor = self.current_text_edit.textCursor()
                            cursor.insertHtml(html_img_tag)

    def apply_text_format(self, format):
        # 应用文本格式
        cursor = self.MainNotes.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.MainNotes.mergeCurrentCharFormat(format)

    # 设置字体
    def font_set(self):
        if self.current_text_edit:
            font, ok = QFontDialog.getFont(self.current_text_edit.currentFont(), self.current_text_edit)
            if ok:
                cursor = self.current_text_edit.textCursor()
                if cursor.hasSelection():
                    fmt = cursor.charFormat()
                    fmt.setFont(font)
                    cursor.setCharFormat(fmt)

    # 关闭窗口后的动作
    def closeEvent(self, event):
        if not self.saved:
            reply = QMessageBox.question(self, "保存更改", "是否要保存更改？",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save()
                self.clear_all_states()
                event.accept()
            elif reply == QMessageBox.No:
                self.clear_all_states()
                event.accept()
            else:
                event.ignore()
        else:
            self.clear_all_states()
            event.accept()

    def clear_all_states(self):
        self.keyWords.clear()
        self.MainNotes.clear()
        self.conclusion.clear()
        self.saved = False
        self.current_text_edit = None
        self.current_filename = None
        self.last_open_directory = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotePage()
    window.show()
    sys.exit(app.exec_())