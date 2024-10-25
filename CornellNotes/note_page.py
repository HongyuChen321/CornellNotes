from ui_note_page import Ui_CornellNotes
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTextEdit, QAction, QFontDialog, QColorDialog
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QColor
import sys

class NotePage(QMainWindow, Ui_CornellNotes):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect()
        self.saved = False
        self.current_text_edit = None

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
        self.spinBox.valueChanged.connect(self.font_size)
        self.fontComboBox.currentFontChanged.connect(self.font_family)

    def new_program(self):
        pass

    def new_note(self):
        self.MainNotes.clear()
        self.keyWords.clear()
        self.conclusion.clear()

    def open(self):
        filename,_ = QFileDialog.getOpenFileName(self, "Open File", "notes", "Note Files (*.note)")
        if filename:
            with open(filename, 'r') as file:
                content = file.read().split('###\n', 2)
                if len(content) == 3:
                    keywords, mainNotes, conclusion = content
                    self.keyWords.setPlainText(keywords)
                    self.MainNotes.setPlainText(mainNotes)
                    self.conclusion.setPlainText(conclusion)

    def save(self):
        pass

    def save_as(self):
        filename,_ = QFileDialog.getSaveFileName(self, "Save File", "notes", "Note Files (*.note)")
        if filename:
            with open(filename, 'w') as file:
                textKeywords = self.keyWords.toPlainText()
                textMainNotes = self.MainNotes.toPlainText()
                textConclusion = self.conclusion.toPlainText()
                file.write(textKeywords + '###\n' + textMainNotes + '###\n' + textConclusion)
            self.saved = True

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
                fmt.setFontWeight(QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal)
                cursor.setCharFormat(fmt)

    def italic(self):
        pass

    def underline(self):
        pass

    def left(self):
        pass

    def right(self):
        self.MainNotes.setAlignment(Qt.AlignRight)
        pass

    def center(self):
        pass

    def left_and_right(self):
        pass

    def superscript(self):
        pass

    def subscript(self):
        pass

    def insert_picture(self):
        pass

    def font_colour(self):
        if self.current_text_edit:
            colour = QColorDialog.getColor(self.current_text_edit.textColor(), self)
            if colour.isValid():
                cursor = self.current_text_edit.textCursor()
                if cursor.hasSelection():
                    fmt = cursor.charFormat()
                    fmt.setForeground(colour)
                    cursor.setCharFormat(fmt)

    def font_size(self):
        pass

    def font_family(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotePage()
    window.show()
    sys.exit(app.exec_())