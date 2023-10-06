from PySide6 import QtCore


def convert_to_parameterised_position(bounding_rect, raw_position):
    return QtCore.QPointF(raw_position.x() / bounding_rect.right(), raw_position.y() / bounding_rect.bottom())


def revert_parameterised_position(bounding_rect, parameterised_position):
    return QtCore.QPointF(bounding_rect.right() * parameterised_position.x(), bounding_rect.bottom() * parameterised_position.y())
