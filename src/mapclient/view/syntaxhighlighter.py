"""
Created on Jul 1, 2015

@author: hsorby
"""
import re

from PySide2 import QtCore, QtGui

rx_success = re.compile('Success: ')
rx_failure = re.compile('Failure: ')


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    def highlightBlock(self, text):
        format_success = QtGui.QTextCharFormat()
        format_success.setForeground(QtCore.Qt.darkGreen)
        format_failure = QtGui.QTextCharFormat()
        format_failure.setForeground(QtCore.Qt.darkRed)

        it = rx_success.finditer(text)
        for match in it:
            span = match.span()
            self.setFormat(match.pos, span[1] - span[0], format_success)

        it = rx_failure.finditer(text)
        for match in it:
            span = match.span()
            self.setFormat(match.pos, span[1] - span[0], format_failure)


