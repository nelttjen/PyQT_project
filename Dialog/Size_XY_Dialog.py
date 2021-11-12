from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic


class SizeError(Exception):
    # для рейза при выходе за 1920x1080
    pass


class Size_XY_Dialog(QDialog):
    def __init__(self, parent, val1, val2, *args):
        super(Size_XY_Dialog, self).__init__(parent, Qt.WindowCloseButtonHint)
        uic.loadUi('./UI/size_xy_change.ui', self)
        self.setFixedSize(211, 131)
        self.setWindowTitle('Редактирование')

        # 2 своих значения
        self.val1 = val1
        self.val2 = val2

        # 2 других значения
        self.additional = args

        self.val1_ed.setText(str(val1))
        self.val2_ed.setText(str(val2))

        self.commit.clicked.connect(self.click_commit)

    def click_commit(self):
        try:
            if self.check_value() and self.check_out_of_bounds():
                self.set_values()
                self.accept()
        except ValueError:
            # отлавливаем что в лайнэдитах не число
            self.error_message('Значения могут быть только числом!')
        except SizeError as e:
            # если выходит за 1920x1080
            self.error_message(e.__str__())

    def check_value(self):
        val1 = int(self.val1_ed.text())
        val2 = int(self.val2_ed.text())
        # проверка на 1920x1080
        if 0 <= val1 <= 1920 and 0 <= val2 <= 1080:
            return True
        else:
            raise SizeError('Максимальные значения:\n1920x1080')

    def check_out_of_bounds(self):
        val1 = int(self.val1_ed.text())
        val2 = int(self.val2_ed.text())
        # проверка на x + sizeX и y + sizeY не выходят за 1920x1080
        if 0 <= val1 + int(self.additional[0]) <= 1920 \
                and 0 <= val2 + int(self.additional[1]) <= 1080:
            return True
        else:
            raise SizeError('Размер изображения выходит за\nпределы картинки')

    def set_values(self):
        # если все проверки пройдены
        self.val1 = self.val1_ed.text()
        self.val2 = self.val2_ed.text()

    def error_message(self, msg="Ошибка при применении"):
        # классический critical
        QMessageBox.critical(self, "Ошибка ", msg, QMessageBox.Ok)

    def exec_(self):
        # возвращение обоих значений
        super(Size_XY_Dialog, self).exec_()
        return self.val1, self.val2
