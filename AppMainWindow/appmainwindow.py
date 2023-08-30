"""
pyuic6 -o AppMainWindow/ui_form.py "path/to/file.ui"
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox, QLabel
from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import QImage, QPixmap, QMouseEvent, QResizeEvent, QKeyEvent
from .ui_form import Ui_MainWindow
from cv2 import Mat, imread, resize, INTER_AREA, INTER_LINEAR
from os import walk
from os.path import join
from time import time


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
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def loadPictures(self, pictures: list[str]) -> None:
        self.resize(600, 500)
        self.pictures = pictures
        self.pic_n = 0
        self._img = None

    def _resize(self, img: Mat, limitSize: tuple[int, int]) -> Mat:
        imgHg, imgWd = img.shape[:2]
        k = imgWd / imgHg

        if limitSize[0] > limitSize[1]:
            newWd, newHg = round(limitSize[1] * k), limitSize[1]
        else:
            newWd, newHg = limitSize[0], round(limitSize[0] / k)

        if (newWd * newHg) < (imgWd * imgHg):
            return resize(img, (newWd, newHg), interpolation=INTER_AREA)
        else:
            return resize(img, (newWd, newHg), interpolation=INTER_LINEAR)

    def drawPicture(self) -> bool:
        if not self.pictures:
            return False
        self._img = imread(self.pictures[self.pic_n])
        if self._img is not None:
            img = self._resize(self._img, (self.width(), self.height()))
            self.setPixmap(cvMatToQPixmap(img))
        self.setWindowTitle(f"Picture-{self.pic_n + 1}")
        return True

    def nextPicture(self) -> bool:
        if (self.pic_n + 1) < len(self.pictures):
            self.pic_n += 1
        else:
            self.pic_n = 0
        return self.drawPicture()

    def prevPicture(self) -> bool:
        if (self.pic_n - 1) > -1:
            self.pic_n -= 1
        else:
            self.pic_n = len(self.pictures) - 1
        return self.drawPicture()

    def resizeEvent(self, ev: QResizeEvent) -> None:
        if self._img is None:
            return
        img = self._resize(self._img, (self.width(), self.height()))
        self.setPixmap(cvMatToQPixmap(img))

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.pos().x() > (self.width() / 2):
            self.nextPicture()
        else:
            self.prevPicture()

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if ev.key() == Qt.Key.Key_Right:
            self.nextPicture()
        elif ev.key() == Qt.Key.Key_Left:
            self.prevPicture()


class AppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.formats = tuple()
        self.picLabel = PictureLabel()

        self.setupUi(self)
        self._init()

    def _init(self) -> None:
        self.searchBtn.clicked.connect(self.searchBtn_clicked)
        self.showBtn.clicked.connect(self.showBtn_clicked)
        self.browseBtn.clicked.connect(self.browseBtn_clicked)
        self.jpeg.setChecked(True)
        self.png.setChecked(True)

    def _prepareFormats(self) -> None:
        formats = list()
        if self.jpeg.isChecked():
            formats.extend([".jpeg", ".jpg", ".jpe", ".jp2"])
        if self.png.isChecked():
            formats.extend([".png"])
        if self.bmp.isChecked():
            formats.extend([".bmp", ".dib"])
        if self.webp.isChecked():
            formats.extend([".webp"])
        if self.ect.isChecked():
            formats.extend([
                ".pbm", ".pgm", ".ppm", ".pxm", ".pnm",
                ".sr", ".ras",
                ".tiff", ".tif",
                ".hdr", ".pic",
            ])
        self.formats = tuple(formats)

    def searchBtn_clicked(self) -> None:
        if not QFileInfo(self.searchDir.text()).isDir():
            QMessageBox.warning(self, "Search process", "Invalid folder")
            return
        self._prepareFormats()
        pictures = list()

        _tm = time()
        for root, dirs, files in walk(self.searchDir.text()):
            pictures.extend(
                [join(root, file) for file in files if file.endswith(self.formats)]
            )
        _tm = time() - _tm

        self.picLabel.loadPictures(pictures)
        QMessageBox.information(
            self,
            "Search process",
            f"Found pictures: {len(pictures)}\nSpent time: {round(_tm)} second(s)",
        )

    def showBtn_clicked(self) -> None:
        if self.picLabel.drawPicture():
            self.picLabel.showMaximized()
        else:
            QMessageBox.warning(self, "Show process", "Nothing to show")

    def browseBtn_clicked(self) -> None:
        _f = QFileDialog.getExistingDirectory(
            self, "Choose a folder to start searching"
        )
        if QFileInfo(_f).isDir():
            self.searchDir.setText(_f)
