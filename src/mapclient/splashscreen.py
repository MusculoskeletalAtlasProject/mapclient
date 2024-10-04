import mapclient.splash_rc

from PySide6 import QtCore, QtGui, QtWidgets

from mapclient.settings.version import __version__ as version


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self._message = ''
        pixmap = QtGui.QPixmap(":/mapclient/splash.png")
        self.setPixmap(pixmap)
        # self._font = QtGui.QFont()
        # self._font.setPixelSize(24)
        self._progress_bar = QtWidgets.QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setGeometry(0, 0, pixmap.width() - int(6 * self.devicePixelRatioF()), 8)
        self._pixmap_height = pixmap.height()
        # self.setFont(self._font)

    def drawContents(self, painter):
        vertical_offset = int(3 * self.devicePixelRatioF())
        self._progress_bar.render(painter, QtCore.QPoint(vertical_offset, self._pixmap_height - 8 - vertical_offset))
        super(SplashScreen, self).drawContents(painter)
        font = QtGui.QFont()
        font.setFamily('Arial')
        pen = QtGui.QPen()
        colour = QtGui.QColor("black")
        colour.setRgb(44, 45, 43)
        pen.setColor(colour)
        painter.setPen(pen)
        font.setPointSize(24)
        painter.setFont(font)
        painter.drawText(550, 320, 120, 40, QtCore.Qt.AlignmentFlag.AlignHCenter, f"v{version}")
        font.setPointSize(18)
        painter.setFont(font)
        painter.drawText(8, 330, 500, 30, QtCore.Qt.AlignmentFlag.AlignLeft, self._message)

    def showMessage(self, message, progress=0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft, color=QtCore.Qt.GlobalColor.black):
        self._progress_bar.setValue(progress)
        self._message = message
        super(SplashScreen, self).showMessage('  ', QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignBottom)
