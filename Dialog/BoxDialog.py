import ctypes

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize


def get_pen(color='red'):
    pen = QPen()
    pen.setWidth(5)
    pen.setBrush(QBrush(QColor(color)))
    return pen


class QTrackClickLabel(QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(QTrackClickLabel, self).__init__(parent=parent)
        self.setMouseTracking(True)
        self.cords = (0, 0)
        self.cord_x = 0
        self.cord_y = 0

    def mousePressEvent(self, event):
        self.cord_x = event.pos().x()
        self.cord_y = event.pos().y()
        self.clicked.emit()

    def get_position(self):
        return self.cord_x, self.cord_y


class BoxDialog(QDialog):
    def __init__(self, parent=None, path=None, values=None):
        super(BoxDialog, self).__init__(parent, Qt.FramelessWindowHint)

        default_size = (1920, 1080)
        user32 = ctypes.windll.user32
        offset = [1.0, 1.0]
        self.user_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.setFixedSize(self.user_size[0], self.user_size[1])
        if self.user_size != default_size:
            offset[0], offset[1] = "{0:.2f}".format(self.user_size[0] / default_size[0]), \
                                   "{0:.2f}".format(self.user_size[1] / default_size[1])
        self.offset = list(map(float, offset))

        self.values = values
        self.path = path
        self.clicks = 0
        self.pos1 = None
        self.pos2 = None
        self.is_done = False

        self.image_qt = QImage(self.path)
        self.image = QTrackClickLabel(self)
        self.btn_commit = QPushButton(self)
        self.btn_clear = QPushButton(self)

        self.image.move(0, 0)
        self.close = QPushButton(self)
        self.init_ui()

        self.clear_image()

    def init_ui(self):
        self.setWindowTitle('Выбор области')

        self.image.resize(self.size())
        self.image.clicked.connect(self.click_on_image)
        self.update_picture()

        self.close.resize(45, 30)
        self.close.move(self.user_size[0] - 45, 0)
        self.close.clicked.connect(self.close_event)
        self.close.setIcon(QIcon('Images/Default/reject.ico'))
        self.close.setIconSize(QSize(45, 24))

        self.btn_commit.setText('Сохранить')
        self.btn_commit.resize(int(110 * self.offset[0]), int(50 * self.offset[1]))
        self.btn_commit.move(int((self.user_size[0] - 110 * self.offset[0])),
                             int((self.user_size[1] - 50 * self.offset[1])))
        self.btn_commit.clicked.connect(self.commit)

        self.btn_clear.setText('Очистить')
        self.btn_clear.resize(int(110 * self.offset[0]), int(50 * self.offset[1]))
        self.btn_clear.move(int((self.user_size[0] - 110 * 2 * self.offset[0])),
                            int((self.user_size[1] - 50 * self.offset[1])))
        self.btn_clear.clicked.connect(self.clear_image)

    def update_picture(self):
        pixmap = QPixmap.fromImage(self.image_qt)
        self.image.setPixmap(pixmap)

    def draw_rect_on_image(self, values=(0, 0, 0, 0), color='red'):
        x, y, size_x, size_y = map(int, values)
        drawer = QPainter(self.image_qt)
        drawer.setPen(get_pen(color))
        drawer.drawRect(x, y, size_x, size_y)

    def clear_image(self):
        self.image_qt = QImage(self.path).scaled(self.user_size[0], self.user_size[1])
        offs_x, offs_y = self.offset
        scaled_values = (self.values[0] * offs_x, self.values[1] * offs_y,
                         self.values[2] * offs_x, self.values[3] * offs_y)
        self.draw_rect_on_image(scaled_values)
        self.update_picture()
        self.clicks = 0
        self.pos1 = None
        self.pos2 = None
        self.is_done = False
        self.btn_commit.hide()
        self.btn_clear.hide()

    def click_on_image(self):
        self.clicks += 1

        if self.clicks == 1:
            self.pos1 = self.sender().get_position()
        if self.clicks == 2:
            self.pos2 = self.sender().get_position()
            self.btn_commit.show()
            self.btn_clear.show()
            x = min(self.pos1[0], self.pos2[0])
            y = min(self.pos1[1], self.pos2[1])
            size_x = max(self.pos1[0], self.pos2[0]) - x
            size_y = max(self.pos1[1], self.pos2[1]) - y
            self.draw_new_rect((x, y, size_x, size_y))
            new_size = list(map(int, [x / self.offset[0], y / self.offset[1],
                                      size_x / self.offset[0], size_y / self.offset[1]]))
            self.pos1 = (new_size[0], new_size[1])
            self.pos2 = (new_size[2], new_size[3])

    def draw_new_rect(self, values, color='green'):
        self.draw_rect_on_image(values=values, color=color)
        self.update_picture()

    def close_event(self):
        self.is_done = False
        self.reject()

    def commit(self):
        self.is_done = True
        self.accept()

    def exec_(self):
        super(BoxDialog, self).exec_()
        # XY, size
        return self.pos1, self.pos2, self.is_done
