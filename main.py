"""
pyinstaller main.py --onefile --windowed --name="Picture Searcher" --icon="resources/search-icon.png"
"""
from PyQt6.QtWidgets import QApplication
from AppMainWindow import AppMainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppMainWindow()
    win.show()
    sys.exit(app.exec())
