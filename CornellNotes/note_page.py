from ui_note_page import Ui_CornellNotes

class NotePage(Ui_CornellNotes):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
        pass

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

    def bold(self):
        pass

    def italic(self):
        pass

    def underline(self):
        pass

    def left(self):
        pass

    def right(self):
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
        pass

    def font_size(self):
        pass

    def font_family(self):
        pass