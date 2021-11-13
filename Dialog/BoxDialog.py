import ctypes

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QBrush, QColor, QPen, QMouseEvent
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize

from Utils.StyleSheet import add_style_sheet


def get_pen(color='red'):
    pen = QPen()
    pen.setWidth(5)
    pen.setBrush(QBrush(QColor(color)))
    return pen


class QFixedButton(QPushButton):
    def __init__(self, parent):
        super(QFixedButton, self).__init__(parent=parent)

    def mouseMoveEvent(self, e: QMouseEvent):
        pass


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

        # получаем отношение экрана пользователя к разрешению картинки 1920x1080
        default_size = (1920, 1080)
        user32 = ctypes.windll.user32
        offset = [1.0, 1.0]
        self.user_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.setFixedSize(self.user_size[0], self.user_size[1])
        if self.user_size != default_size:
            offset[0], offset[1] = "{0:.2f}".format(self.user_size[0] / default_size[0]), \
                                   "{0:.2f}".format(self.user_size[1] / default_size[1])
        self.offset = list(map(float, offset))

        # default_values
        self.values = values
        self.path = path
        self.clicks = 0
        self.pos1 = None
        self.pos2 = None
        self.is_done = False

        # widgets
        self.image_qt = QImage(self.path)
        self.image = QTrackClickLabel(self)
        self.btn_commit = QFixedButton(self)
        self.btn_clear = QFixedButton(self)
        self.close = QFixedButton(self)

        # Functions
        self.init_ui()
        self.clear_image()

    def init_ui(self):
        self.setWindowTitle('Выбор области')

        self.image.resize(self.size())
        self.image.clicked.connect(self.click_on_image)
        self.image.move(0, 0)
        self.update_picture()

        self.close.resize(45, 30)
        self.close.move(self.user_size[0] - 45, 0)
        self.close.clicked.connect(self.close_event)
        self.close.setIcon(QIcon('Images/Default/reject.ico'))
        self.close.setIconSize(QSize(45, 24))

        self.btn_commit.setText('Сохранить')
        # подгоняем кнопку под разрешение экрана пользователя
        self.btn_commit.resize(int(110 * self.offset[0]), int(50 * self.offset[1]))
        self.btn_commit.move(int((self.user_size[0] - 110 * self.offset[0])),
                             int((self.user_size[1] - 50 * self.offset[1])))
        self.btn_commit.clicked.connect(self.commit)

        self.btn_clear.setText('Очистить')
        # подгоняем кнопку под разрешение экрана пользователя
        self.btn_clear.resize(int(110 * self.offset[0]), int(50 * self.offset[1]))
        self.btn_clear.move(int((self.user_size[0] - 110 * 2 * self.offset[0])),
                            int((self.user_size[1] - 50 * self.offset[1])))
        self.btn_clear.clicked.connect(self.clear_image)

        add_style_sheet([self.btn_commit, self.btn_clear])

    def update_picture(self):
        # обновляет картинку из хранящегося image_qt
        pixmap = QPixmap.fromImage(self.image_qt)
        self.image.setPixmap(pixmap)

    def draw_rect_on_image(self, values=(0, 0, 0, 0), color='red'):
        # рисует прямоугольник на image_qt по заданным величинам (x, y, sizeX, sizeY)
        x, y, size_x, size_y = map(int, values)
        drawer = QPainter(self.image_qt)
        drawer.setPen(get_pen(color))
        drawer.drawRect(x, y, size_x, size_y)

    def click_on_image(self):
        # выззывается при клике на картинку, первые 2 нажатия рисуют прямоугольник - будущий бокс текста/картинки
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
            self.draw_rect_on_image((x, y, size_x, size_y), color='green')
            self.update_picture()
            new_size = list(map(int, [x / self.offset[0], y / self.offset[1],
                                      size_x / self.offset[0], size_y / self.offset[1]]))
            self.pos1 = (new_size[0], new_size[1])
            self.pos2 = (new_size[2], new_size[3])

    def clear_image(self):
        # очищает возвращает всё на дефолтные значения
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

    def close_event(self):
        # кнопка закрытия слева вверху
        self.is_done = False
        self.reject()

    def commit(self):
        # кнопка применить
        self.is_done = True
        self.accept()

    def exec_(self):
        super(BoxDialog, self).exec_()
        # XY, size
        return self.pos1, self.pos2, self.is_done
