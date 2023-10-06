from PySide6 import QtCore


def convert_to_parameterised_position(bounding_rect, raw_position):
    print(raw_position.x() / bounding_rect.width(), raw_position.x(), bounding_rect.width(), bounding_rect.left())
    return QtCore.QPointF(raw_position.x() / bounding_rect.width(), raw_position.y() / bounding_rect.height())


def revert_parameterised_position(bounding_rect, parameterised_position):
    print(bounding_rect.width() * parameterised_position.x(), parameterised_position.x(), bounding_rect.width(), bounding_rect.left())
    return QtCore.QPointF(bounding_rect.width() * parameterised_position.x(), bounding_rect.height() * parameterised_position.y())
