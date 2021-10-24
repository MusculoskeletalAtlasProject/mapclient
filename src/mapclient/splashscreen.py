import mapclient.splash_rc

from PySide2 import QtCore, QtGui, QtWidgets


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        pixmap = QtGui.QPixmap(":/mapclient/splash.png")
        self.setPixmap(pixmap)
        self._font = QtGui.QFont()
        self._font.setPixelSize(20)
        self._progress_bar = QtWidgets.QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setGeometry(0, 0, pixmap.width() - 0, 8)
#         self.setStyleSheet("""
# QProgressBar {
#     border: 2px solid grey;
#     border-radius: 5px;
# }
#
# QProgressBar::chunk {
#     background-color: #05B8CC;
#     width: 20px;
# }        """)
        self._pixmap_height = pixmap.height()
        self.setFont(self._font)

    def drawContents(self, painter):
        self._progress_bar.render(painter, QtCore.QPoint(0, self._pixmap_height - 8))
        super(SplashScreen, self).drawContents(painter)

    def showMessage(self, message, progress=0):
        self._progress_bar.setValue(progress)
        super(SplashScreen, self).showMessage('  ' + message, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
