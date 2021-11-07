import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton, QColorDialog
from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon
from PyQt5 import uic

from PIL import Image, ImageDraw, ImageFont
import sys
import shutil

from Dialog.AgreementDialog import AgreementDialog
from Dialog.PatternDialog import PatternDialog

from Pattern.Pattern import find_pattern_by_id
from Pattern.RegPatterns import recreate_patterns

from Utils.Pallite import create_palette
from Utils.SortPatterns import sort_patterns
from Utils.Delimiter import text_delimiter
from Utils.AlphaConverter import convert_image
from Utils.ChangeCSV import restore_default_csv, change_color
from Utils.Path import get_name_from_path


class Window(QMainWindow):
    def __init__(self, p_list):
        super().__init__()
        self.VERSION = '1.23'
        self.APP_NAME = 'Meme Generator'

        # UI
        uic.loadUi('./UI/MainScreen.ui', self)
        self.setWindowTitle(f'{self.APP_NAME} v{self.VERSION}')
        self.setWindowIcon(QIcon('./Images/Default/logo.png'))
        self.setObjectName('MainScreen')
        self.setFixedSize(1080, 860)

        # DEFAULT VALUES
        self.previewSize = (854, 540)
        self.patterns = p_list

        self.flag = False
        self.img1 = None
        self.img2 = None
        self.img_pattern = None

        self.update_pixmap('Images/Default/default.png')

        # color
        self.btn_color = QPushButton(self)
        self.btn_color.resize(30, 30)

        self.btn_color_restore = QPushButton(self)
        self.btn_color_restore.resize(30, 30)
        self.btn_color_restore.move(30, 0)
        self.btn_color_restore.setText('D')

        # Functions
        self.btn_connect()
        self.update_edits()

    def btn_connect(self):
        self.btn_clear.clicked.connect(self.clear_all)
        self.btn_pattern.clicked.connect(self.set_pattern)

        self.btn_preview.clicked.connect(self.update_preview)
        self.btn_save.clicked.connect(self.save_meme)

        self.image1.clicked.connect(self.set_img)
        self.image2.clicked.connect(self.set_img)

        self.btn_color.clicked.connect(self.change_color)
        self.btn_color_restore.clicked.connect(self.default_color)

        color_pixmap = QIcon('./Images/Default/palette.png')
        self.btn_color.setIcon(color_pixmap)

    def clear_all(self):
        self.update_pixmap('Images/Default/default.png')
        self.img_pattern = None
        self.flag = False
        self.clear_image()
        self.update_edits()

    def set_pattern(self):
        # Вызов диалога выбора шаблонов
        try:
            dialog = PatternDialog(self, pattern_list=self.patterns)
            dialog.show()
            # получение данных
            pattern_id, self.patterns = dialog.exec_()
            if not pattern_id:
                # Если просто закрыли окно
                return
            pattern_id = get_name_from_path(pattern_id)
            # Поиск выбранного шаблона
            self.img_pattern = find_pattern_by_id(self.patterns, pattern_id)
            # обновляет поля под новый шаблон
            self.update_edits(self.img_pattern)
            self.update_img_info()

            # сохранение редактируемого шаблона и картинки для показа в приложении
            img = Image.open(f'Images/Patterns/{pattern_id}.png')
            img.save('Images/Temp/img_patternTemp.png')
            img_preview = img.resize(self.previewSize)
            img_preview.save('Images/Preview/preview.png')
            self.update_pixmap()
            print(self.img_pattern)
        except Exception as e:
            self.clear_all()
            print(e)

    def update_pixmap(self, path='Images/Preview/preview.png'):
        # Меняет картинку на главном экране
        self.img_preview.setPixmap(QPixmap(path))

    def update_preview(self):
        # Кнопка Применить, пересоздает картинку и отображает её
        if self.img_pattern:
            self.flag = self.recreate_image()
            self.update_pixmap()

    def recreate_image(self):
        # Пересоздает мем и сохраняет его в Output
        if self.img_pattern:
            meme = Image.open('Images/Temp/img_patternTemp.png').convert('RGB')
            draw = ImageDraw.Draw(meme)
            flag = False
            # Сам процесс создания картинки
            if self.img_pattern[1][0] and self.lineEdit1.text():
                self.draw_text(draw, 1)
                flag = True
            if self.img_pattern[2][0] and self.lineEdit2.text():
                self.draw_text(draw, 2)
                flag = True
            if self.img_pattern[3][0] and self.img1:
                self.img1 = self.draw_image(self.img1, 1, meme)
                flag = True
            if self.img_pattern[4][0] and self.img2:
                self.img2 = self.draw_image(self.img2, 2, meme)
                flag = True
            meme.save('Images/Output/output.png')
            img_preview = meme.resize(self.previewSize)
            img_preview.save('Images/Preview/preview.png')
            # Возвращает были ли какие-то изменения шаблона
            return flag

    def update_edits(self, pattern=None):
        # обновление полей при установке нового шаблона либо отчистке
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

            self.flag = False
        else:
            self.line1.hide()
            self.line2.hide()
            self.lineEdit1.hide()
            self.lineEdit2.hide()
            self.image1.hide()
            self.image2.hide()
            self.image1Info.hide()
            self.image2Info.hide()
        # удаление старого мема
        try:
            os.remove('./Images/Output/output.png')
        except FileNotFoundError:
            pass
        self.lineEdit1.setText('')
        self.lineEdit2.setText('')
        self.img1 = None
        self.img2 = None
        self.image1Info.setText('Картинка 1\nне загружена')
        self.image2Info.setText('Картинка 2\nне загружена')

    def set_img(self):
        # Кнопка загрузить картинку, загружается pillow изображение
        if self.img_pattern:
            if self.sender().text()[-1] == '1' and self.img_pattern[3][0]:
                self.img1 = self.choose_image(1)
            elif self.sender().text()[-1] == '2' and self.img_pattern[4][0]:
                self.img2 = self.choose_image(2)
            self.update_img_info()
        else:
            # если вдруг что-то пошло не так
            self.clear_image()

    def choose_image(self, img_id):
        # диалог выбора картинки
        try:
            f_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку...', '.', "Image (*.png *.jpg *jpeg)")
            # проверка, выбрана ли картинка
            if f_name[0]:
                f_image = Image.open(f_name[0])
                print(f_image.mode)
                # фикс чеерного фона при имеющимся канале прозрачности
                if f_image.mode[-1] == 'A':
                    f_image = f_image.convert('RGBA')
                    f_image = convert_image(f_image)
                return f_image
            # если картинка не выбрана - оставить картинки, которые уже есть
            elif img_id == 1:
                return self.img1
            elif img_id == 2:
                return self.img2
        # ошибки при открытии картинок
        except PermissionError:
            QMessageBox.critical(self, "Ошибка ", "Невозможно открыть файл (Отказано в доступе)", QMessageBox.Ok)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Ошибка ", "Невозможно открыть файл", QMessageBox.Ok)

    def clear_image(self):
        # удалить обе загружеенные картинки
        self.img1 = None
        self.img2 = None
        self.update_img_info()

    def update_img_info(self):
        # апдейтер информации о загрузкее картинок
        text1 = 'Картинка 1\nзагруженна' if self.img1 else 'Картинка 1\nне загруженна'
        text2 = 'Картинка 2\nзагруженна' if self.img2 else 'Картинка 2\nне загруженна'
        self.image1Info.setText(text1)
        self.image2Info.setText(text2)

        self.update_img_palette()

    def update_img_palette(self):
        # апдейтер цвета информации о загрузкее картинок
        pal = self.image1Info.palette()
        pal.setColor(QPalette.WindowText, QColor("green" if self.img1 else "red"))
        self.image1Info.setPalette(pal)

        pal = self.image2Info.palette()
        pal.setColor(QPalette.WindowText, QColor("green" if self.img2 else "red"))
        self.image2Info.setPalette(pal)

    def save_meme(self):
        # скрипт сохранения мема
        if self.flag:
            # получение пути
            filepath, props = QFileDialog.getSaveFileName(self, 'Сохранить как...', "meme.png",
                                                          "Image (*.png *.jpg *jpeg)")
            if not filepath:
                # Если окошко закрыли
                return
            try:
                # проверка на наличие мема в папке Images/Output
                if not os.path.exists('./Images/Output/output.png'):
                    raise FileNotFoundError('Ошибка сохранения: Файл был удален или перемещен\n'
                                            'Попробуйте пересоздать мем, нажав кнопку "Применить"')
                shutil.copy2('./Images/Output/output.png', filepath)
            # ошибки, которые могут выскочить при сохранении
            except PermissionError:
                QMessageBox.critical(self, "Ошибка ", "Не удалось сохранить файл (Отказано в доступе!)",
                                     QMessageBox.Ok)
            except FileNotFoundError as e:
                QMessageBox.critical(self, "Ошибка ", e.__str__(),
                                     QMessageBox.Ok)
        else:
            # Если шаблона нет, либо ничего не выбрано
            text = "Не выбран шаблон!" if not self.img_pattern else "Вы ничего не изменили в шаблоне!"
            QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)

    def change_color(self):
        # дииалог выбора цвета
        color = QColorDialog.getColor()
        if color.getRgb()[:-1] != (0, 0, 0):
            self.set_color(color)

    def set_color(self, color):
        # Кнопка палитры, изменяет задний фон приложения
        key_id = self.objectName()
        change_color(color, key_id)
        self.change_palette(key_id)

    def default_color(self):
        # Кнопка отката, откатывает задний фон до начального значения
        sure = AgreementDialog(self, 'Вы действительно хотите\nвостановить значение по умолчанию?').exec_()
        if sure:
            key_id = self.objectName()
            restore_default_csv(key_id, isFullRestore=False)
            self.change_palette(key_id)

    def change_palette(self, key_id):
        # меняет задний фон при изменении цвета
        self.setPalette(create_palette(key_id))

    def draw_text(self, draw, text_id):
        # вставляет текст в картинку
        try:
            size, position, text_size, delim, align = get_text_items(self.img_pattern[text_id])
            line_text = self.lineEdit1.text() if text_id == 1 else self.lineEdit2.text()
            text, w, h, font = get_text(line_text, text_size, delim, draw)
            position = get_position(size, position, w, h, align)
            draw.text(position,
                      text,
                      fill=(255, 255, 255), font=font,
                      align="center", stroke_width=2 + int(text_size / 40), stroke_fill=(0, 0, 0))
        except Exception as e:
            print(e.__str__())

    def draw_image(self, image, image_id, target):
        # Вставляет картинку в target и возвращает её
        try:
            size = self.img_pattern[image_id + 2][2]
            position = self.img_pattern[image_id + 2][1]
            image = image.resize(size)
            target.paste(image, position)
            return image
        except Exception as e:
            print(e.__str__())


def get_text(text, text_size, delim, draw):
    # Возвращает все хар-ки текста (разделенный текст, высота, ширина, шрифт)
    if 0 < delim < len(text.split()):
        text = text_delimiter(text, delim)
    font = ImageFont.truetype("arial.ttf", text_size)
    w, h = draw.textsize(text, font=font)
    h += 20 * delim
    return text, w, h, font


def get_text_items(prop_list: list):
    # Возвращает хар-ки текста из шаблона
    return prop_list[2], prop_list[1], prop_list[3], prop_list[4], prop_list[5]


def get_position(size, position, w, h, align='center'):
    # ищет позицию, на которой будет писаться текст
    if align == 'center':
        position = (((size[0] - w) / 2) + position[0], ((size[1] - h) / 2) + position[1])
    elif align == 'left':
        position = (position[0], ((size[1] - h) / 2) + position[1])
    elif align == 'right':
        position = (position[0] + size[0] - w, ((size[1] - h) / 2) + position[1])
    # В этом случае текст будет писаться слево вверху
    return position


def resize_patterns():
    # проверка основных картинок на соответствие размеру
    base_path = './Images/Patterns'
    objects = sort_patterns(os.listdir(base_path)[:-1])
    for i in objects:
        try:
            temp_img = Image.open(f'{base_path}/{i}')
            if temp_img.size != (1920, 1080):
                temp_img = temp_img.resize((1920, 1080))
                temp_img.save(f'{base_path}/{i}')
        except FileNotFoundError:
            continue
    # Проверка preview картинок на соответствие размеру
    base_path = './Images/Patterns/Preview'
    objects = sort_patterns(os.listdir(base_path))
    for i in objects:
        try:
            temp_img = Image.open(f'{base_path}/{i}')
            if temp_img.size != (284, 190):
                temp_img = temp_img.resize((284, 190))
                temp_img.save(f'{base_path}/{i}')
        except FileNotFoundError:
            continue


def check_preview_patterns():
    # Проверка наличия preview изображений
    previews = os.listdir('./Images/Patterns/Preview')
    patterns = os.listdir('./Images/Patterns')[:-1]
    previews = sort_patterns(previews)
    patterns = sort_patterns(patterns)
    if len(previews) != len(patterns):
        for i in patterns:
            if i not in previews:
                try:
                    shutil.copy(f'./Images/Patterns/{i}', f'./Images/Patterns/Preview/{i}')
                except PermissionError:
                    continue


def init_app():
    # подготовка перед запуском приложения
    check_preview_patterns()
    resize_patterns()
    return recreate_patterns()


if __name__ == '__main__':
    # создание окна и запуск приложения
    list_patterns = init_app()
    app = QApplication(sys.argv)
    f = Window(list_patterns)
    f.setPalette(create_palette('MainScreen'))
    f.show()
    sys.exit(app.exec_())
