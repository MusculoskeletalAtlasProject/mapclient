
from PySide6 import QtWidgets, QtCore


class MessageBox(QtWidgets.QMessageBox):
    def __init__(self, icon, title, text, buttons, parent=None, close_after=None):
        """
        An extension of the QtWidgets.QMessageBox class that automatically closes itself after a set number of seconds. This class allows the user
        to pass an additional argument (close_after) to specify how long the MessageBox should be displayed for before it closes. 
        The close_after parameter is specified in units of seconds. If the close_after argument is set to zero, the MessageBox 
        will not be displayed.

        Parameters
        ----------
        icon: PySide6.QtWidgets.QMessageBox.Icon
        title: str
        text: str
        buttons: PySide6.QtWidgets.QMessageBox.StandardButtons
        parent: PySide6.QtWidgets.QWidget, optional
        close_after: float, optional
        """
        super().__init__(icon, title, text, buttons, parent=parent)
        self._close_after = close_after * 1000
        QtCore.QTimer.singleShot(self._close_after, self.accept)

    def exec_(self):
        # Only display the MessageBox if the close timer is greater than 0.
        if self._close_after > 0:
            super().exec()
