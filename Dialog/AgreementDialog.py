from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class AgreementDialog(QDialog):
    def __init__(self, parrent=None, text=''):
        super().__init__(parrent, Qt.WindowCloseButtonHint)

        uic.loadUi('./UI/agreement.ui', self)
        self.setWindowTitle('Подтверждение')

        self.label.setText(text)
        self.label.move(20, 13)
        self.label.resize(self.label.sizeHint())
        self.setFixedSize(self.label.sizeHint().width() + 40, 91)
        self.buttonBox.move((self.size().width() - self.buttonBox.size().width()) / 2, 61)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
