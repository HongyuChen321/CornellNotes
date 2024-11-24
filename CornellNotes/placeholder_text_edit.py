from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt

class PlaceholderTextEdit(QTextEdit):
    def __init__(self, placeholder_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder_text = placeholder_text
        self.setPlaceholderText(self.placeholder_text)
        self.textChanged.connect(self.check_placeholder)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if self.toPlainText() == self.placeholder_text:
            self.clear()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.toPlainText():
            self.setPlaceholderText(self.placeholder_text)

    def check_placeholder(self):
        if not self.toPlainText():
            self.setPlaceholderText(self.placeholder_text)
        else:
            self.setPlaceholderText('')