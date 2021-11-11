from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

from Dialog.Size_XY_Dialog import Size_XY_Dialog
from Utils.AlphaConverter import convert_image
from Utils.Free_ID import get_free_id

from Utils.Values import CREATE as CREATE_MODE
from Utils.Values import CHANGE as CHANGE_MODE
from Utils.Values import CHANGE_DEFAULT as DEFAULT_CHANGE_MODE

from Utils.Values import INFO_SIZE, INFO_POSITION, NEW_PATTERN_PATH


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


def none_list(times: int):
    return [None for _ in range(times)]


class PatternError(Exception):
    pass


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
        self.has_image_changed = False

        self.create_text1 = False
        self.create_text2 = False
        self.create_image1 = False
        self.create_image2 = False

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
        self.change_pattern.clicked.connect(self.set_new_pattern)

        pattern = {1: 'text1_Size', 2: 'text1_XY',
                   3: 'text2_Size', 4: 'text2_XY',
                   5: 'image1_Size', 6: 'image1_XY',
                   7: 'image2_Size', 8: 'image2_XY'
                   }
        for i, val in enumerate(self.get_connects()):
            val[0].clicked.connect(self.set_value)
            val[0].setObjectName(pattern[i + 1])
        self.create_connect()

    def commit(self):
        if self.mode == CHANGE_MODE or self.mode == DEFAULT_CHANGE_MODE:
            new_list, is_crashed = self.create_new_list()
            if not is_crashed:
                self.new_list = new_list
                self.accept()
        else:
            new_list, is_crashed = self.create_new_pattern()
            if not is_crashed:
                self.new_list = new_list
                self.has_changes = True
                self.accept()

    def list_1(self):
        return self.get_text_list(self.text1_XY_info, self.text1_Size_info,
                                  self.text1_textSize, self.text1_delimiter,
                                  self.get_text_aligns(1), 1)

    def list_2(self):
        return self.get_text_list(self.text2_XY_info, self.text2_Size_info,
                                  self.text2_textSize, self.text2_delimiter,
                                  self.get_text_aligns(2), 2)

    def create_new_list(self):
        crash = False
        if self.pattern[1][0]:
            list_1, crash = self.list_1()
            if self.pattern[1] != list_1 and not crash:
                self.has_changes = True
        else:
            list_1 = none_list(6)
        if self.pattern[2][0]:
            list_2, crash = self.list_2()
            if self.pattern[2] != list_2 and not crash:
                self.has_changes = True
        else:
            list_2 = none_list(6)
        if self.pattern[3][0]:
            xy, size = get_xy_size(self.image1_XY_info, self.image1_Size_info)
            list_3 = [1, xy, size]
            if self.pattern[3] != list_3 and not crash:
                self.has_changes = True
        else:
            list_3 = none_list(3)
        if self.pattern[4][0]:
            xy, size = get_xy_size(self.image2_XY_info, self.image2_Size_info)
            list_4 = [1, xy, size]
            if self.pattern[4] != list_4 and not crash:
                self.has_changes = True
        else:
            list_4 = none_list(3)

        # pack Values
        if self.mode == CHANGE_MODE:
            pack = [self.path, list_1, list_2, list_3, list_4, False]
        else:
            pack = [self.path, list_1, list_2, list_3, list_4, True]
        return pack, crash

    def create_new_pattern(self):
        try:
            crash = False
            if self.path != NEW_PATTERN_PATH:
                raise PatternError('Шаблон не загружен')
            # text1
            if not any([self.create_text1, self.create_text2, self.create_image1, self.create_image2]):
                raise PatternError('Выберите, что должно находится на шаблоне')
            if self.create_text1:
                list_1, crash = self.list_1()
            else:
                list_1 = none_list(6)
            # text2
            if self.create_text2:
                list_2, crash = self.list_2()
            else:
                list_2 = none_list(6)
            # image1
            if self.create_image1:
                xy, size = get_xy_size(self.image1_XY_info, self.image1_Size_info)
                list_3 = [1, xy, size]
            else:
                list_3 = none_list(3)
            # image2
            if self.create_image2:
                xy, size = get_xy_size(self.image2_XY_info, self.image2_Size_info)
                list_4 = [1, xy, size]
            else:
                list_4 = none_list(3)
            pack = [self.path, list_1, list_2, list_3, list_4, False, get_free_id()]
            return pack, crash
        except PatternError as e:
            crash = True
            self.error_message(e.__str__())
            return None, crash

    def get_text_aligns(self, text_id):
        if text_id == 1:
            return [self.text1_align_left, self.text1_align_center, self.text1_align_right]
        if text_id == 2:
            return [self.text2_align_left, self.text2_align_center, self.text2_align_right]

    def error_message(self, msg="error"):
        QtWidgets.QMessageBox.critical(self, "Ошибка ", msg, QtWidgets.QMessageBox.Ok)

    def get_text_list(self, target1, target2, target3, target4, targets5, text_id):
        crash = False
        enabled = 1
        xy, size = get_xy_size(target1, target2)
        try:
            scale = int(target3.text())
            if not 0 < scale < 300:
                raise ValueError
        except ValueError:
            self.error_message('Ошибка:\nТекст 1: Размер шрифта\n'
                               'Не может быть текстом или <= 0\nНе может быть больше 300')
            crash = True
            return None, crash
        try:
            delim = int(target4.text())
            if delim < 0:
                crash = True
                raise ValueError
        except ValueError:
            self.error_message('Ошибка:\nТекст 1: Слов на строке\nНе может быть текстом или отрицательным числом')
            return None, crash
        if self.mode in (CHANGE_MODE, CREATE_MODE):
            align = get_align_from_buttons(targets5)
        else:
            align = self.pattern[text_id][5]
        return [enabled, xy, size, scale, delim, align], crash

    def create_connect(self):
        self.image1_enable.clicked.connect(self.update_create_fields)
        self.image2_enable.clicked.connect(self.update_create_fields)
        self.text1_enable.clicked.connect(self.update_create_fields)
        self.text2_enable.clicked.connect(self.update_create_fields)

    def update_create_fields(self):
        if self.text1_enable.isChecked():
            enable_handler(self.text1_textSize, self.text1_delimiter, self.get_text_aligns(1),
                           self.text1_Size, self.text1_XY, self.text1)
            self.create_text1 = True
        else:
            disable_handler(self.text1_textSize, self.text1_delimiter, self.get_text_aligns(1),
                            self.text1_Size, self.text1_XY, self.text1)
            self.create_text1 = False
        if self.text2_enable.isChecked():
            enable_handler(self.text2_textSize, self.text2_delimiter, self.get_text_aligns(2),
                           self.text2_Size, self.text2_XY, self.text2)
            self.create_text2 = True
        else:
            disable_handler(self.text2_textSize, self.text2_delimiter, self.get_text_aligns(2),
                            self.text2_Size, self.text2_XY, self.text2)
            self.create_text2 = False
        if self.image1_enable.isChecked():
            enable_handler(t_XY=self.image1_XY, t_Size=self.image1_Size, t_box=self.image1)
            self.create_image1 = True
        else:
            disable_handler(t_XY=self.image1_XY, t_Size=self.image1_Size, t_box=self.image1)
            self.create_image1 = False
        if self.image2_enable.isChecked():
            enable_handler(t_XY=self.image2_XY, t_Size=self.image2_Size, t_box=self.image2)
            self.create_image2 = True
        else:
            disable_handler(t_XY=self.image2_XY, t_Size=self.image2_Size, t_box=self.image2)
            self.create_image2 = False

    def set_new_pattern(self):
        f_path = QFileDialog.getOpenFileName(self, 'Выбрать картинку...', '.', "Image (*.png *.jpg *jpeg)")[0]
        print(f_path)
        if f_path:
            pixmap_handler(self.pattern_preview, QPixmap(f_path))
            new_pattern = Image.open(f_path)
            if new_pattern.mode[-1] == 'A':
                new_pattern = convert_image(new_pattern.convert('RGBA'))
            new_pattern = new_pattern.resize((1920, 1080))
            new_pattern.save(NEW_PATTERN_PATH)
            self.path = NEW_PATTERN_PATH
            if self.mode != CREATE_MODE:
                self.has_image_changed = [True, self.pattern[0]]

    def get_connects(self):
        connects = [[self.text1_Size, self.text1_Size_info],
                    [self.text1_XY, self.text1_XY_info],
                    [self.text2_Size, self.text2_Size_info],
                    [self.text2_XY, self.text2_XY_info],
                    [self.image1_Size, self.image1_Size_info],
                    [self.image1_XY, self.image1_XY_info],
                    [self.image2_Size, self.image2_Size_info],
                    [self.image2_XY, self.image2_XY_info]]
        return connects

    def set_value(self):
        connects = self.get_connects()
        for i, cell in enumerate(connects):
            if cell[0].objectName() == self.sender().objectName():
                name = cell[0].objectName()
                if name in ('text1_Size', 'text2_Size', 'image1_Size', 'image2_Size'):
                    val1, val2 = cell[1].text().replace(INFO_SIZE, '').split('x')
                    val3, val4 = connects[i + 1][1].text().replace(INFO_POSITION, '') \
                        .replace('X: ', '').replace('Y:', '').split(', ')
                    new_val1, new_val2 = Size_XY_Dialog(self, val1, val2, val3, val4).exec_()
                    cell[1].setText(f'{INFO_SIZE}{new_val1}x{new_val2}')
                else:
                    val1, val2 = cell[1].text().replace(INFO_POSITION, '')\
                        .replace('X: ', '').replace('Y:', '').split(', ')
                    val3, val4 = connects[i - 1][1].text().replace(INFO_SIZE, '').split('x')
                    new_val1, new_val2 = Size_XY_Dialog(self, val1, val2, val3, val4).exec_()
                    cell[1].setText(f'{INFO_POSITION}X: {new_val1}, Y: {new_val2}')

    def exec_(self):
        super(ChangeDialog, self).exec_()
        return self.new_list, self.has_changes, self.has_image_changed
