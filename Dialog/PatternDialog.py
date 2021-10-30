# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogPattern.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

from Utils.Pallite import createPallite


class DoubleClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mouseDoubleClickEvent(self, event):
        try:
            self.clicked.emit()
        except Exception as e:
            print(e)


class PatternDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(PatternDialog, self).__init__(parent=parent)
        self.setObjectName("Dialog")
        self.setWindowTitle('Выбор шаблона')
        self.setFixedSize(923, 650)
        self.returnVal = None
        self.list_patterns = []

        # self.buttonBox = QtWidgets.QDialogButtonBox(self)
        # self.setButtonBox()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        self.patterns = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layout.addWidget(self.scrollArea)

        self.scrollArea.setPalette(createPallite('PatternDialog'))
        self.scrollAreaWidgetContents.setPalette(createPallite('PatternDialog'))
        self.setPalette(createPallite('PatternDialog'))


        flag = True
        for j in range(10):
            if flag:
                for i in range(3):
                    try:
                        pathToImg = f'Images/Patterns/Preview/pattern{(j * 3 + i) + 1}.png'
                        try:
                            open(pathToImg)
                        except IOError as e:
                            flag = False
                            print(e.__str__())
                            break
                        if flag:
                            pixmap = QtGui.QPixmap(pathToImg)
                            label = DoubleClickLabel()
                            label.setPixmap(pixmap)
                            label.setObjectName(f"pattern{(j * 3 + i) + 1}")
                            label.clicked.connect(self.doubleClick)
                            self.patterns.addWidget(label, j, i)

                            self.list_patterns.append([label, pathToImg])
                    except Exception as e:
                        print(e)

    def doubleClick(self):
        try:
            for i in self.list_patterns:
                if self.sender() == i[0]:
                    self.returnVal = i[1]
                    self.accept()
        except Exception as e:
            print(e)
            self.reject()

    def exec_(self):
        super(PatternDialog, self).exec_()
        return self.returnVal
