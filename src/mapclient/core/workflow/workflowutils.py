from PySide6 import QtCore


def convert_to_parameterised_position(bounding_rect, raw_position, offset):
    return QtCore.QPointF(raw_position.x() / (bounding_rect.width() - offset.x()), raw_position.y() / (bounding_rect.height() - offset.y()))


def revert_parameterised_position(bounding_rect, parameterised_position, offset):
    return QtCore.QPointF((bounding_rect.width() - offset.x()) * parameterised_position.x(), (bounding_rect.height() - offset.y()) * parameterised_position.y())
