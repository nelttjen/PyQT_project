import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5 import uic


class AgreementDialog(QDialog):
    def __init__(self, parrent=None, text=''):
        super().__init__(parrent, Qt.WindowCloseButtonHint)

        uic.loadUi('./UI/agreement.ui', self)
        self.setWindowTitle('Подтверждение')
        self.setFixedSize(221, 91)

        self.label.setText(text)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)




