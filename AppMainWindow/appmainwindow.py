"""
pyuic6 -o AppMainWindow/ui_form.py "path/to/file.ui"
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox, QLabel
from PyQt6.QtCore import QFileInfo
from PyQt6.QtGui import QImage, QPixmap, QMouseEvent
from .ui_form import Ui_MainWindow
from cv2 import Mat, imread, resize, INTER_AREA
from os import walk
from os.path import join


def cvMatToQImage(inMat: Mat) -> QImage:
    height, width, channel = inMat.shape
    bytesPerLine = 3 * width
    qImg = QImage(inMat.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
    return qImg.rgbSwapped()


def cvMatToQPixmap(inMat: Mat) -> QPixmap:
    return QPixmap.fromImage(cvMatToQImage(inMat))


class PictureLabel(QLabel):
    def __init__(self, pictures: list[str] = None) -> None:
        super().__init__()
        self.loadPictures(pictures)
        self.setText("")

    def loadPictures(self, pictures: list[str]) -> None:
        self.pictures = pictures
        self.pic_n = 0

    def drawPicture(self) -> None:
        img = imread(self.pictures[self.pic_n])
        self.resize(img.shape[1], img.shape[0])
        self.setPixmap(cvMatToQPixmap(img))
        self.setWindowTitle(f"Picture-{self.pic_n + 1}")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        isNext = event.pos().x() > (self.width() / 2)
        if isNext:
            if (self.pic_n + 1) < len(self.pictures):
                self.pic_n += 1
            else:
                self.pic_n = 0
        else:
            if (self.pic_n - 1) > -1:
                self.pic_n -= 1
            else:
                self.pic_n = len(self.pictures) - 1
        self.drawPicture()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


class AppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.stopSearch = False
        self.formats = tuple()
        self.picLabel = PictureLabel()

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
        pictures = list()

        for root, dirs, files in walk(self.searchDir.text()):
            if self.stopSearch:
                break
            pictures.extend(
                [
                    join(root, file)
                    for file in files
                    if (not self.stopSearch and file.endswith(self.formats))
                ]
            )
        self.picLabel.loadPictures(pictures)

        message = f"{len(pictures)} pictures have been found"
        QMessageBox.information(self, "Search process", message)

    def stopBtn_clicked(self) -> None:
        self.stopSearch = True

    def showBtn_clicked(self) -> None:
        self.picLabel.drawPicture()
        self.picLabel.showNormal()

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
