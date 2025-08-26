from PySide6 import QtWidgets


class EditProfileDialog(QtWidgets.QDialog):
    """
    Dialog for editing the name of a plugin profile.
    """

    def __init__(self, current_profile_name, parent=None):
        super(EditProfileDialog, self).__init__(parent)
        self.setWindowTitle("Edit Profile")
        self.setMinimumSize(300, 150)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Enter the new name for the profile:")
        self.layout.addWidget(self.label)

        self.profileNameInput = QtWidgets.QLineEdit(self)
        self.profileNameInput.setText(current_profile_name)
        self.layout.addWidget(self.profileNameInput)

        self.layout.addSpacerItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

    def getProfileName(self):
        return self.profileNameInput.text().strip()