import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDialog
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5 import uic

from PIL import Image
import sys

from Pattern.PatternDialog import PatternDialog
from Utils.Pallite import createPallite
from Utils.SortPatterns import sortPatterns
from Pattern.Pattern import registerPatterns, findPattermById


class Window(QMainWindow):
    def __init__(self, p_list):
        super().__init__()
        self.VERSION = 1.0
        self.APP_NAME = 'Meme Generator'

        # UI
        uic.loadUi('MainScreen.ui', self)
        self.setWindowTitle(f'{self.APP_NAME} v{self.VERSION}')
        self.setFixedSize(1080, 860)

        # DEFAULT VALUES
        self.previewSize = (854, 540)
        self.val = None
        self.patterns = p_list
        self.img_pattern = None

        self.pixmap = QPixmap('Images/Default/default.png')
        self.img_preview.setPixmap(self.pixmap)
        self.img = Image.open('Images/Default/default.png')

        # Functions
        self.btn_connect()
        self.updateEdits()

    def btn_connect(self):
        self.btn_clear.clicked.connect(self.clearPreview)
        self.btn_pattern.clicked.connect(self.setPattern)

    def clearPreview(self):
        self.pixmap = QPixmap('Images/Default/default.png')
        self.img_preview.setPixmap(self.pixmap)
        self.img_pattern = None
        self.val = None

    def setPattern(self):
        try:
            dialog = PatternDialog(self)
            palette = createPallite('PatternDialog')
            f.setPalette(palette)
            dialog.show()
            self.val = dialog.exec_()
        except Exception as e:
            print(e)
        try:
            if not self.val:
                print('Null returned')
                return
            # self.img = Image.new(mode='RGB', size=(1920, 1080), color=(0, 60, 0))
            self.val = str(self.val).replace('Images/Patterns/Preview/', '')
            self.img = Image.open(f'Images/Patterns/{self.val}')
            for i in self.patterns:
                if i.getObject()[0].replace('Images/Patterns/', '').replace('./', '').replace('.png', '') == \
                        self.val.replace('.png', ''):
                    self.img_pattern = i.getObject()
                    break
                else:
                    self.img_pattern = None
            self.updateEdits(self.img_pattern)
            img_preview = self.img.resize(self.previewSize)
            img_preview.save('Images/Temp/img_Temp.png')
            self.setPixmap()
        except Exception as e:
            self.clearPreview()
            print(e)

    def setPixmap(self, path='Images/Temp/img_Temp.png'):
        self.pixmap = QPixmap(path)
        self.img_preview.setPixmap(self.pixmap)

    def updatePreview(self, pattern=None):
        if pattern:
            pass

    def updateEdits(self, pattern=None):
        if pattern:
            self.line1.show() if pattern[1][0] else self.line1.hide()
            self.lineEdit1.show() if pattern[1][0] else self.lineEdit1.hide()
            self.lineEdit1.setReadOnly(False) if pattern[1][0] else self.lineEdit1.setReadOnly(True)
            self.line2.show() if pattern[2][0] else self.line2.hide()
            self.lineEdit2.show() if pattern[2][0] else self.lineEdit2.hide()
            self.lineEdit2.setReadOnly(False) if pattern[2][0] else self.lineEdit2.setReadOnly(True)

            self.image1.show() if pattern[3][0] else self.image1.hide()
            self.image1Info.show() if pattern[3][0] else self.image1Info.hide()
            self.image2.show() if pattern[4][0] else self.image2.hide()
            self.image2Info.show() if pattern[4][0] else self.image2Info.hide()
        else:
            self.line1.hide()
            self.line2.hide()
            self.lineEdit1.hide()
            self.lineEdit2.hide()
            self.image1.hide()
            self.image2.hide()
            self.image1Info.hide()
            self.image2Info.hide()


def resizePatterns():
    basePath = './Images/Patterns'
    objects = sortPatterns(os.listdir(basePath)[:-1])
    for i in objects:
        try:
            temp_img = Image.open(f'{basePath}/{i}')
            if temp_img.size != (1920, 1080):
                temp_img = temp_img.resize((1920, 1080))
                temp_img.save(f'{basePath}/{i}')
        except Exception as e:
            continue
    basePath = './Images/Patterns/Preview'
    objects = sortPatterns(os.listdir(basePath))
    for i in objects:
        try:
            temp_img = Image.open(f'{basePath}/{i}')
            if temp_img.size != (284, 190):
                temp_img = temp_img.resize((284, 190))
                temp_img.save(f'{basePath}/{i}')
        except Exception as e:
            continue


def checkPreviewPatterns():
    previews = os.listdir('./Images/Patterns/Preview')
    patterns = os.listdir('./Images/Patterns')[:-1]
    previews = sortPatterns(previews)
    patterns = sortPatterns(patterns)
    if len(previews) != len(patterns):
        for i in patterns:
            if i not in previews:
                try:
                    copy = Image.open(f'./Images/Patterns/{i}')
                    copy.save(f'./Images/Patterns/Preview/{i}')
                except PermissionError as e:
                    continue


def initApp():
    checkPreviewPatterns()
    resizePatterns()
    value = registerPatterns()
    return value


if __name__ == '__main__':
    list_patterns = initApp()
    app = QApplication(sys.argv)
    f = Window(list_patterns)
    palette = createPallite('MainScreen')
    f.setPalette(palette)
    f.show()
    sys.exit(app.exec_())
