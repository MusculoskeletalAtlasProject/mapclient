
from PySide2 import QtWidgets, QtCore


class MessageBox(QtWidgets.QMessageBox):
    def __init__(self, icon, title, text, buttons, parent=None, close_after=None):
        super().__init__(icon, title, text, buttons, parent=parent)
        self._close_after = close_after * 1000
        QtCore.QTimer.singleShot(self._close_after, self.accept)

    def exec_(self):
        # Only display the MessageBox if the close timer is greater than 0.
        if self._close_after > 0:
            super().exec_()
