from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

CREATE_MODE = 0
CHANGE_MODE = 1
DEFAULT_CHANGE_MODE = 2

INFO_SIZE = 'Текущий размер:\n'
INFO_POSITION = 'Текущее положение:\n'


def format_text(position=(0, 0), size=(0, 0)):
    info_pos = INFO_POSITION + f'X: {position[0]}, Y: {position[1]}'
    info_size = INFO_SIZE + f'{size[0]}x{size[1]}'
    return info_pos, info_size


def pixmap_handler(target, pixmap):
    pixmap = pixmap.scaled(target.size())
    target.setPixmap(pixmap)


def disable_pixmap(target):
    target.setEnabled(False)


def text_handler(t_textSize=None, t_Delimiter=None, t_Align=None, t_XY=None, t_Size=None,
                 textSize=1, textDelimiter=0, text_XY=(0, 0), text_Size=(1, 1)):
    t_textSize.setText(str(textSize)) if t_textSize else None
    t_Delimiter.setText(str(textDelimiter)) if t_Delimiter else None
    t_Align.setChecked(True) if t_Align else None
    position_text, size_text = format_text(text_XY, text_Size)
    t_XY.setText(position_text) if t_XY else None
    t_Size.setText(size_text) if t_Size else None


def image_handler(t_XY=None, t_Size=None, image_XY=(0, 0), image_size=(1, 1)):
    position_image, size_image = format_text(image_XY, image_size)
    t_XY.setText(position_image) if t_XY else None
    t_Size.setText(size_image) if t_Size else None


def get_align_from_str(variants, str_align):
    # variants pattern:
    # left, center, right
    if str_align == 'left':
        return variants[0]
    if str_align == 'center':
        return variants[1]
    if str_align == 'right':
        return variants[2]
    return variants[1]


def get_align_from_buttons(buttons):
    for i, button in enumerate(buttons):
        if button.isChecked():
            if i == 0:
                return 'left'
            if i == 1:
                return 'center'
            if i == 2:
                return 'right'


def get_text_props(props_list):
    # textSize, delimiter, position, size
    return props_list[3], props_list[4], props_list[1], props_list[2]


def get_image_props(props_list):
    # position, size
    return props_list[1], props_list[2]


def disable_handler(t_textSize=None, t_Delimiter=None, t_Aligns=None, t_XY=None, t_Size=None, t_box=None):
    if t_textSize:
        t_textSize.setReadOnly(True)
        t_textSize.setText('')
    if t_Delimiter:
        t_Delimiter.setReadOnly(True)
        t_Delimiter.setText('')
    if t_Aligns:
        for i in t_Aligns:
            i.setCheckable(False)
    if t_XY:
        t_XY.setEnabled(False)
    if t_Size:
        t_Size.setEnabled(False)
    if t_box:
        t_box.setTitle(t_box.title().replace(' (Отключено)', '') + ' (Отключено)')


def enable_handler(t_textSize=None, t_Delimiter=None, t_Aligns=None, t_XY=None, t_Size=None, t_box=None):
    if t_textSize:
        t_textSize.setReadOnly(False)
        t_textSize.setText('1')
    if t_Delimiter:
        t_Delimiter.setReadOnly(False)
        t_Delimiter.setText('0')
    if t_Aligns:
        for i in t_Aligns:
            i.setCheckable(True)
            if i.objectName() == 'text1_align_center' or i.objectName() == 'text2_align_center':
                i.setChecked(True)
    if t_XY:
        t_XY.setEnabled(True)
    if t_Size:
        t_Size.setEnabled(True)
    if t_box:
        t_box.setTitle(t_box.title().replace(' (Отключено)', ''))


def window_title(mode):
    if mode == CREATE_MODE:
        return 'Создание шаблона'
    if mode == CHANGE_MODE:
        return 'Редактирование шаблона'
    if mode == DEFAULT_CHANGE_MODE:
        return 'Редактирование базового шаблона'


def get_xy_size(target1, target2):
    xy = tuple(map(int, target1.text().replace('X: ', '').replace('Y: ', '')
                   .replace('Текущее положение:\n', '').split(', ')))
    size = tuple(map(int, target2.text().replace('Текущий размер:\n', '').split('x')))
    return xy, size


class ChangeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, mode=1, pattern=None):
        super(ChangeDialog, self).__init__(parent, Qt.WindowCloseButtonHint)
        uic.loadUi('./UI/change.ui', self)
        self.setObjectName("ChangeDialog")
        self.setFixedSize(651, 571)
        self.setWindowTitle(window_title(mode))

        self.pattern = pattern
        self.mode = mode

        self.new_list = None
        self.has_changes = False
        if mode in (CHANGE_MODE, DEFAULT_CHANGE_MODE):
            self.path = self.pattern[0]
        else:
            self.path = './Images/Default/default.png'

        self.prepare_ui()

        self.connect_buttons()

    def prepare_ui(self):
        if self.mode == CREATE_MODE:
            self.create_prepare()
        if self.mode == CHANGE_MODE:
            self.change_prepare()
        if self.mode == DEFAULT_CHANGE_MODE:
            self.default_change_prepare()

    def create_prepare(self):
        text_handler(self.text1_textSize, self.text1_delimiter, self.text1_align_center,
                     self.text1_XY_info, self.text1_Size_info)
        text_handler(self.text2_textSize, self.text2_delimiter, self.text2_align_center,
                     self.text2_XY_info, self.text2_Size_info)
        image_handler(self.image1_XY_info, self.image1_Size_info)
        image_handler(self.image2_XY_info, self.image2_Size_info)
        disable_handler(self.text1_textSize, self.text1_delimiter, self.get_text_aligns(1),
                        self.text1_XY, self.text1_Size, self.text1)
        disable_handler(self.text2_textSize, self.text2_delimiter, self.get_text_aligns(2),
                        self.text2_XY, self.text2_Size, self.text2)
        disable_handler(t_XY=self.image1_XY, t_Size=self.image1_Size, t_box=self.image1)
        disable_handler(t_XY=self.image2_XY, t_Size=self.image2_Size, t_box=self.image2)
        pixmap = QPixmap(self.path)
        pixmap_handler(self.pattern_preview, pixmap)

    def change_prepare(self):
        self.creationBox.hide()
        # text1
        if self.pattern[1][0]:
            align = get_align_from_str(self.get_text_aligns(1), self.pattern[1][5])
            text_size, delim, pos, size = get_text_props(self.pattern[1])
            text_handler(self.text1_textSize, self.text1_delimiter, align,
                         self.text1_XY_info, self.text1_Size_info,
                         textSize=text_size, textDelimiter=delim,
                         text_XY=pos, text_Size=size)
        else:
            disable_handler(self.text1_textSize, self.text1_delimiter, self.get_text_aligns(1),
                            self.text1_Size, self.text1_XY, self.text1)

        # text2
        if self.pattern[2][0]:
            align = get_align_from_str(self.get_text_aligns(2), self.pattern[2][5])
            text_size, delim, pos, size = get_text_props(self.pattern[2])
            text_handler(self.text2_textSize, self.text2_delimiter, align,
                         self.text2_XY_info, self.text2_Size_info,
                         textSize=text_size, textDelimiter=delim,
                         text_XY=pos, text_Size=size)
        else:
            disable_handler(self.text2_textSize, self.text2_delimiter, self.get_text_aligns(2),
                            self.text2_Size, self.text2_XY, self.text2)

        # image1
        if self.pattern[3][0]:
            position, size = get_image_props(self.pattern[3])
            image_handler(self.image1_XY_info, self.image1_Size_info,
                          image_XY=position, image_size=size)
        else:
            disable_handler(t_XY=self.image1_XY, t_Size=self.image1_Size, t_box=self.image1)

        # image 2
        if self.pattern[4][0]:
            position, size = get_image_props(self.pattern[4])
            image_handler(self.image2_XY_info, self.image2_Size_info,
                          image_XY=position, image_size=size)
        else:
            disable_handler(t_XY=self.image2_XY, t_Size=self.image2_Size, t_box=self.image2)
        pixmap = QPixmap(self.path)
        pixmap_handler(self.pattern_preview, pixmap)

    def default_change_prepare(self):
        self.creationBox.hide()
        # text1
        if self.pattern[1][0]:
            text_handler(t_textSize=self.text1_textSize, t_Delimiter=self.text1_delimiter,
                         t_XY=self.text1_XY_info, t_Size=self.text1_Size_info,
                         textSize=self.pattern[1][3], textDelimiter=self.pattern[1][4],
                         text_XY=self.pattern[1][1], text_Size=self.pattern[1][2])
            disable_handler(t_Aligns=self.get_text_aligns(1),
                            t_XY=self.text1_XY, t_Size=self.text1_Size)
        else:
            disable_handler(self.text1_textSize, self.text1_delimiter, self.get_text_aligns(1),
                            self.text1_Size, self.text1_XY, self.text1)
        # text2
        if self.pattern[2][0]:
            text_handler(t_textSize=self.text2_textSize, t_Delimiter=self.text2_delimiter,
                         t_XY=self.text2_XY_info, t_Size=self.text2_Size_info,
                         textSize=self.pattern[2][3], textDelimiter=self.pattern[2][4],
                         text_XY=self.pattern[2][1], text_Size=self.pattern[2][2])
            disable_handler(t_Aligns=self.get_text_aligns(2),
                            t_XY=self.text2_XY, t_Size=self.text2_Size)
        else:
            disable_handler(self.text2_textSize, self.text2_delimiter, self.get_text_aligns(2),
                            self.text2_Size, self.text2_XY, self.text2)
        # image1
        if self.pattern[3][0]:
            position, size = get_image_props(self.pattern[3])
            print(position, size)
            image_handler(self.image1_XY_info, self.image1_Size_info,
                          image_XY=position, image_size=size)
        disable_handler(t_XY=self.image1_XY, t_Size=self.image1_Size, t_box=self.image1)
        # image2
        if self.pattern[4][0]:
            position, size = get_image_props(self.pattern[4])
            image_handler(self.image2_XY_info, self.image2_Size_info,
                          image_XY=position, image_size=size)
        disable_handler(t_XY=self.image2_XY, t_Size=self.image2_Size, t_box=self.image2)
        pixmap = QPixmap(self.path)
        pixmap_handler(self.pattern_preview, pixmap)
        disable_pixmap(self.change_pattern)

    def connect_buttons(self):
        self.save_button.clicked.connect(self.commit)

        self.create_connect()

    def commit(self):
        print(self.pattern)
        if self.mode == CHANGE_MODE or self.mode == DEFAULT_CHANGE_MODE:
            new_list = self.create_new_list()
            print(new_list)
            print(self.has_changes)
            if new_list:
                self.accept()

    def create_new_list(self):
        if self.pattern[1][0]:
            list_1 = self.get_text_list(self.text1_XY_info, self.text1_Size_info,
                                        self.text1_textSize, self.text1_delimiter,
                                        self.get_text_aligns(1), 1)
            if self.pattern[1] != list_1:
                self.has_changes = True
        else:
            list_1 = [None for _ in range(6)]
        if self.pattern[2][0]:
            list_2 = self.get_text_list(self.text2_XY_info, self.text2_Size_info,
                                        self.text2_textSize, self.text2_delimiter,
                                        self.get_text_aligns(2), 2)
            if self.pattern[2] != list_2:
                self.has_changes = True
        else:
            list_2 = [None for _ in range(6)]
        if self.pattern[3][0]:
            xy, size = get_xy_size(self.image1_XY_info, self.image1_Size_info)
            list_3 = [1, xy, size]
            if self.pattern[3] != list_3:
                self.has_changes = True
        else:
            list_3 = [None for _ in range(3)]
        if self.pattern[4][0]:
            xy, size = get_xy_size(self.image2_XY_info, self.image2_Size_info)
            list_4 = [1, xy, size]
            if self.pattern[4] != list_4:
                self.has_changes = True
        else:
            list_4 = [None for _ in range(3)]
        pack = [self.path, list_1, list_2, list_3, list_4, self.pattern[5]]
        return pack

    def get_text_aligns(self, text_id):
        if text_id == 1:
            return [self.text1_align_left, self.text1_align_center, self.text1_align_right]
        if text_id == 2:
            return [self.text2_align_left, self.text2_align_center, self.text2_align_right]

    def error_message(self, msg="error"):
        QtWidgets.QMessageBox.critical(self, "Ошибка ", msg, QtWidgets.QMessageBox.Ok)

    def get_text_list(self, target1, target2, target3, target4, target5, text_id):
        enabled = 1
        xy, size = get_xy_size(target1, target2)
        try:
            scale = int(target3.text())
            if not 0 < scale < 300:
                raise ValueError
        except ValueError:
            self.error_message('Ошибка:\nТекст 1: Размер шрифта\n'
                               'Не может быть текстом или <= 0\nНе может быть больше 300')
            return
        try:
            delim = int(target4.text())
            if delim < 0:
                raise ValueError
        except ValueError:
            self.error_message('Ошибка:\nТекст 1: Слов на строке\nНе может быть текстом или отрицательным числом')
            return
        if self.mode == CHANGE_MODE and target5:
            align = get_align_from_buttons(self.get_text_aligns(1))
        else:
            align = self.pattern[text_id][5]
        return [enabled, xy, size, scale, delim, align]

    def create_connect(self):
        self.image1_enable.clicked.connect(self.update_create_fields)
        self.image2_enable.clicked.connect(self.update_create_fields)
        self.text1_enable.clicked.connect(self.update_create_fields)
        self.text2_enable.clicked.connect(self.update_create_fields)

    def update_create_fields(self):
        if self.text1_enable.isChecked():
            enable_handler(self.text1_textSize, self.text1_delimiter, self.get_text_aligns(1),
                           self.text1_Size, self.text1_XY, self.text1)
        else:
            disable_handler(self.text1_textSize, self.text1_delimiter, self.get_text_aligns(1),
                            self.text1_Size, self.text1_XY, self.text1)
        if self.text2_enable.isChecked():
            enable_handler(self.text2_textSize, self.text2_delimiter, self.get_text_aligns(2),
                           self.text2_Size, self.text2_XY, self.text2)
        else:
            disable_handler(self.text2_textSize, self.text2_delimiter, self.get_text_aligns(2),
                            self.text2_Size, self.text2_XY, self.text2)
        if self.image1_enable.isChecked():
            enable_handler(t_XY=self.image1_XY, t_Size=self.image1_Size, t_box=self.image1)
        else:
            disable_handler(t_XY=self.image1_XY, t_Size=self.image1_Size, t_box=self.image1)
        if self.image2_enable.isChecked():
            enable_handler(t_XY=self.image2_XY, t_Size=self.image2_Size, t_box=self.image2)
        else:
            disable_handler(t_XY=self.image2_XY, t_Size=self.image2_Size, t_box=self.image2)

    def exec_(self):
        super(ChangeDialog, self).exec_()
        if self.mode in (CHANGE_MODE, DEFAULT_CHANGE_MODE):
            return self.new_list, self.has_changes, self.mode
        return self.new_list, self.has_changes
