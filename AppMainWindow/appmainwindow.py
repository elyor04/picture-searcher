"""
pyuic6 -o AppMainWindow/ui_form.py "path/to/file.ui"
"""
from PyQt6.QtWidgets import QMainWindow, QWidget
from .ui_form import Ui_MainWindow


class AppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
