"""
pyuic6 -o AppMainWindow/ui_form.py "path/to/file.ui"
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QFileDialog
from PyQt6.QtCore import QFileInfo
from .ui_form import Ui_MainWindow


class AppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.setupUi(self)
        self._init()

    def _init(self) -> None:
        self.browseBtn.clicked.connect(self.browseBtn_clicked)
        self.searchBtn.clicked.connect(self.searchBtn_clicked)
        self.stopBtn.clicked.connect(self.stopBtn_clicked)
        self.showBtn.clicked.connect(self.showBtn_clicked)

    def browseBtn_clicked(self) -> None:
        _f = QFileDialog.getExistingDirectory(
            self, "Choose a folder to start searching"
        )
        if QFileInfo(_f).isDir():
            self.searchDir.setText(_f)

    def searchBtn_clicked(self) -> None:
        pass

    def stopBtn_clicked(self) -> None:
        pass

    def showBtn_clicked(self) -> None:
        pass
