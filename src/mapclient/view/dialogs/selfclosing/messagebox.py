
from PySide2 import QtWidgets, QtCore


class MessageBox(QtWidgets.QMessageBox):

    close_after = None

    def __init__(self, icon, title, text, buttons, parent=None):
        super().__init__(icon, title, text, buttons, parent=parent)
        QtCore.QTimer.singleShot(self.close_after, self.accept)

    def exec_(self):
        # Only display the MessageBox if the close timer is greater than 0.
        if self.close_after > 0:
            super().exec_()
