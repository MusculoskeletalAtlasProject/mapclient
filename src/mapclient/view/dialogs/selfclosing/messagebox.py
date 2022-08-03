
from PySide2 import QtWidgets, QtCore


class MessageBox(QtWidgets.QMessageBox):

    def __init__(self, icon, title, text, buttons, parent=None, close_after=2000):
        super().__init__(icon, title, text, buttons, parent=parent)
        QtCore.QTimer.singleShot(close_after, self.accept)
