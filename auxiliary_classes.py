
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

class UnsavedFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Warning!")

        QBtn = (QDialogButtonBox.StandardButton.Discard | QDialogButtonBox.StandardButton.Cancel)

        self.buttonBox = QDialogButtonBox(QBtn)

        self.layout = QVBoxLayout()
        message = QLabel("Changes not saved. Do you want to continue?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Discard).clicked.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.reject)