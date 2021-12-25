# from .editor import Editor


# if __name__ == "__main__":
#     ed = Editor()
#     ed.run()

#     ed.quit()

from PyQt6.QtWidgets import QApplication
import sys

from window import Window

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())