"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland

This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""
import logging
import re

from functools import wraps
from PySide6 import QtCore, QtGui, QtWidgets

from mapclient.exceptions import ClientRuntimeError
from mapclient.view.dialogs.error.errordialog import ErrorDialog

logger = logging.getLogger(__name__)


rx_success = re.compile('Success: ')
rx_failure = re.compile('Failure: ')


def create_default_image_icon(name):
    """
    The default image size is 512x512
    """
    image = QtGui.QImage(':/workflow/images/default_step_icon.png')
    if name:
        p = QtGui.QPainter(image)

        text_width = 0.9 * image.size().width()
        text_height = 0.2 * image.size().height()
        text_padding = 0.05 * image.size().height()
        rect = p.fontMetrics().boundingRect(0, 0, text_width, 0,
                                            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.TextFlag.TextWordWrap,
                                            name)
        factor = text_height / rect.height()
        f = p.font()
        f.setPointSizeF(f.pointSizeF() * factor)
        p.setFont(f)

        # Updated text rect
        rect = p.fontMetrics().boundingRect(0, 0, text_width, 0,
                                            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.TextFlag.TextWordWrap,
                                            name)
        # Draw the text with a background rectangle
        pen = QtGui.QPen()
        pen.setWidth(11)
        pen.setColor(QtCore.Qt.GlobalColor.black)
        p.setPen(pen)
        p.setBrush(QtCore.Qt.GlobalColor.darkGray)

        rect.moveTo((image.size().width() - rect.width()) / 2, (image.height() - rect.height()) / 2)
        background_rect = rect.adjusted(-text_padding, -text_padding, text_padding, text_padding)

        p.drawRoundedRect(background_rect, text_padding / 2, text_padding / 2)
        p.setPen(QtCore.Qt.GlobalColor.white)
        p.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.TextFlag.TextWordWrap, name)

    return image


def set_wait_cursor(f):
    """
    Decorator to a gui action method (e.g. methods in QtGui.QWidget) to
    set and unset a wait cursor and unset after the method is finished.
    """

    @wraps(f)
    def do_wait_cursor(*a, **kw):
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
            return f(*a, **kw)
        except Exception:
            raise
        finally:
            # Always unset
            QtWidgets.QApplication.restoreOverrideCursor()

    return do_wait_cursor


def handle_runtime_error(f):
    """
    Decorator to a gui action so that all exceptions raised will result
    in user notification via a dialog.
    """

    @wraps(f)
    def do_runtime_error(self, *a, **kw):
        try:
            return f(self, *a, **kw)
        except ClientRuntimeError as e:
            QtWidgets.QApplication.restoreOverrideCursor()
            logger.error('{0}: {1}'.format(e.title, e.description))
            ErrorDialog(e.title, e.description, self).exec()
    return do_runtime_error


def is_light_mode():
    return QtGui.QGuiApplication.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Light


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):

    def highlightBlock(self, text):
        format_success = QtGui.QTextCharFormat()
        format_success.setForeground(QtCore.Qt.GlobalColor.darkGreen)
        format_failure = QtGui.QTextCharFormat()
        format_failure.setForeground(QtCore.Qt.GlobalColor.darkRed)

        it = rx_success.finditer(text)
        for match in it:
            span = match.span()
            self.setFormat(match.pos, span[1] - span[0], format_success)

        it = rx_failure.finditer(text)
        for match in it:
            span = match.span()
            self.setFormat(match.pos, span[1] - span[0], format_failure)
