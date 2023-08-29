"""
pyuic6 -o AppMainWindow/ui_form.py "path/to/file.ui"
"""
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import QFileInfo
from .ui_form import Ui_MainWindow
from os import walk
from os.path import join


class AppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.stopSearch = False
        self.formats = tuple()
        self.pictures = list()

        self.setupUi(self)
        self._init()

    def _init(self) -> None:
        self.startBtn.clicked.connect(self.startBtn_clicked)
        self.stopBtn.clicked.connect(self.stopBtn_clicked)
        self.showBtn.clicked.connect(self.showBtn_clicked)
        self.browseBtn.clicked.connect(self.browseBtn_clicked)
        self.all.clicked.connect(self.all_clicked)
        self.jpeg.setChecked(True)
        self.png.setChecked(True)

    def _prepareFormats(self) -> None:
        formats = list()
        if self.all.isChecked():
            formats.extend(
                [".jpeg", ".jpg", ".jpe", ".jp2", ".png", ".bmp", ".dib", ".webp"]
            )
        else:
            if self.jpeg.isChecked():
                formats.extend([".jpeg", ".jpg", ".jpe", ".jp2"])
            if self.png.isChecked():
                formats.extend([".png"])
            if self.bmp.isChecked():
                formats.extend([".bmp", ".dib"])
            if self.webp.isChecked():
                formats.extend([".webp"])
        self.formats = tuple(formats)

    def startBtn_clicked(self) -> None:
        if not QFileInfo(self.searchDir.text()).isDir():
            return
        self.stopSearch = False
        self._prepareFormats()
        self.pictures.clear()

        for root, dirs, files in walk(self.searchDir.text()):
            if self.stopSearch:
                break
            self.pictures.extend(
                [
                    join(root, file)
                    for file in files
                    if (not self.stopSearch and file.endswith(self.formats))
                ]
            )

    def stopBtn_clicked(self) -> None:
        self.stopSearch = True

    def showBtn_clicked(self) -> None:
        print(self.pictures)

    def browseBtn_clicked(self) -> None:
        _f = QFileDialog.getExistingDirectory(
            self, "Choose a folder to start searching"
        )
        if QFileInfo(_f).isDir():
            self.searchDir.setText(_f)

    def all_clicked(self) -> None:
        formats = [self.jpeg, self.png, self.bmp, self.webp]
        if self.all.isChecked():
            for f in formats:
                f.setChecked(True)
                f.setEnabled(False)
        else:
            self.jpeg.setChecked(True)
            self.png.setChecked(True)
            self.bmp.setChecked(False)
            self.webp.setChecked(False)
            for f in formats:
                f.setEnabled(True)
