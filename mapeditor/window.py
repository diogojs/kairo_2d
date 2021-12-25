from PyQt6.QtWidgets import QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kairo Map Editor")
        self.setFixedSize(1280, 720)
