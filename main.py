import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDialog
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5 import uic

from PIL import Image, ImageDraw, ImageFont
import sys
import shutil

from Pattern.PatternDialog import PatternDialog
from Utils.Pallite import createPallite
from Utils.SortPatterns import sortPatterns
from Pattern.Pattern import registerPatterns


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

        self.img1 = None
        self.img2 = None

        self.img_text1 = None
        self.img_text2 = None

        self.pixmap = QPixmap('Images/Default/default.png')
        self.img_preview.setPixmap(self.pixmap)
        self.img = Image.open('Images/Default/default.png')

        # Functions
        self.btn_connect()
        self.updateEdits()

    def btn_connect(self):
        self.btn_clear.clicked.connect(self.clearPreview)
        self.btn_pattern.clicked.connect(self.setPattern)

        self.btn_preview.clicked.connect(self.updatePreview)

    def clearPreview(self):
        self.pixmap = QPixmap('Images/Default/default.png')
        self.img_preview.setPixmap(self.pixmap)
        self.img_pattern = None
        self.val = None
        self.updateEdits()

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

            self.img.save('Images/Temp/img_patternTemp.png')
            img_preview = self.img.resize(self.previewSize)
            img_preview.save('Images/Preview/preview.png')
            self.setPixmap()
            print(self.img_pattern)
        except Exception as e:
            self.clearPreview()
            print(e)

    def setPixmap(self, path='Images/Preview/preview.png'):
        self.pixmap = QPixmap(path)
        self.img_preview.setPixmap(self.pixmap)

    def updatePreview(self):
        if self.img_pattern:
            self.recreateImage()
            self.setPixmap()

    def recreateImage(self):
        if self.img_pattern:
            meme = Image.open('Images/Temp/img_patternTemp.png').convert('RGBA')
            meme_pixels = meme.load()
            if self.img_pattern[1][0]:
                try:
                    size = self.img_pattern[1][2]
                    position = self.img_pattern[1][1]
                    text_size = self.img_pattern[1][3]
                    text = self.lineEdit1.text() + '\n или пидорас?' + '\n или пидорас?'
                    self.img_text1 = Image.new("RGBA", size, (0, 0, 0, 0))
                    draw = ImageDraw.Draw(self.img_text1)
                    font = ImageFont.truetype("arial.ttf", text_size)
                    w, h = draw.textsize(text, font=font)
                    draw.text(((size[0] - w) / 2, (size[1] - h) / 2),
                              text,
                              fill=(255, 255, 255), font=font,
                              align="center", stroke_width=2 + int(text_size / 40), stroke_fill=(0, 0, 0))
                    self.img_text1.save('Images/Temp/img_text1Temp.png')
                    text1_pixels = self.img_text1.load()
                    for x in range(position[0], position[0] + size[0]):
                        for y in range(position[1], position[1] + size[1]):
                            r, g, b, a = text1_pixels[x - position[0], y - position[1]]
                            if a != 0:
                                meme_pixels[x, y] = r, g, b, a
                except Exception as e:
                    print(e.__str__())
            meme.save('Images/Output/output.png')
            img_preview = meme.resize(self.previewSize)
            img_preview.save('Images/Preview/preview.png')

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
        self.lineEdit1.setText('')
        self.lineEdit2.setText('')
        self.img1 = None
        self.img2 = None
        self.image1Info.setText('Картинка 1\nне загружена')
        self.image2Info.setText('Картинка 2\nне загружена')


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
                    shutil.copy(f'./Images/Patterns/{i}', f'./Images/Patterns/Preview/{i}')
                    # copy = Image.open(f'./Images/Patterns/{i}')
                    # copy.save(f'./Images/Patterns/Preview/{i}')
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
