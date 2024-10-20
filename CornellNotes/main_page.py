from ui_main_page import Ui_MainPage

class MainPage(Ui_MainPage):
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
