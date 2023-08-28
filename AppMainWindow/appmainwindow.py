from PyQt6.QtWidgets import QMainWindow, QWidget


class AppMainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
