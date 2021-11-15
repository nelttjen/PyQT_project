import os
import requests

from Utils.ChangeCSV import restore_default_csv
from Utils.Pallite import load_csv
from Utils.Values import CSS_DEFAULT, GIT_CONTENT_URL, DEFAULT_PATTERNS_COUNT


# Проверка на присутвтсие ВСЕХ файлов для работы программы
def check_all_data():
    return all([check_exists(), check_data(), check_ui(), check_images()])


def check_data():
    db_path = './Data/patterns.db'
    csv_path = './Data/Background.csv'
    style_path = './Data/style.css'
    try:
        if not os.path.exists(db_path):
            try:
                print('База данных не обнаружена, скачивание...')
                download(db_path[2:])
            except Exception as e:
                print(e.__str__())
                return False
        if not os.path.exists(csv_path):
            restore_default_csv('full', True)
        else:
            data = load_csv()
            if not data:
                restore_default_csv('restore', True)
        if not os.path.exists(style_path):
            with open(style_path, 'w', newline='') as css_file:
                css_file.write(CSS_DEFAULT)
    except (PermissionError, FileNotFoundError, FileExistsError):
        return False
    return True


def check_exists():
    first = True
    ui_path = './UI'
    data_path = './Data'
    images_path_main = './Images'
    images_path_default = './Images/Default'
    images_path1 = './Images/Temp'
    images_path2 = './Images/Preview'
    images_path3 = './Images/Output'
    images_path4 = './Images/Patterns'
    images_path5 = './Images/Patterns/Preview'
    list_path = [ui_path, data_path, images_path_main, images_path_default,
                 images_path1, images_path2, images_path3, images_path4, images_path5]
    try:
        for path in list_path:
            if not os.path.exists(path):
                if first:
                    print('Некоторые папки не обнаружены, создание...')
                    first = False
                os.makedirs(path)
    except (PermissionError, FileNotFoundError, FileExistsError):
        return False
    return True


def check_ui():
    ui1_path = 'UI/agreement.ui'
    ui2_path = 'UI/change.ui'
    ui3_path = 'UI/MainScreen.ui'
    ui_paths = [ui1_path, ui2_path, ui3_path]
    for path in ui_paths:
        if not os.path.exists(path):
            try:
                download(path)
            except Exception as e:
                print(e.__str__())
                return False
    return True


def check_images():
    first = True
    path = 'Images/Patterns'
    file_paths = []
    for p_id in range(1, DEFAULT_PATTERNS_COUNT + 1):
        file_paths.append(f'{path}/pattern{p_id}.png')
    for path in file_paths:
        if not os.path.exists(path):
            try:
                if first:
                    print('Обнаружено повреждение изображений, восстановление...')
                    first = False
                download(path)
            except Exception as e:
                print(e.__str__())
                return False
    path = 'Images/Default/'
    file_names = ['default.png', 'icon.ico', 'logo.png', 'palette.png', 'reject.ico', 'trashcan.jpg']
    for name in file_names:
        if not os.path.exists(path + name):
            try:
                if first:
                    print('Обнаружено повреждение изображений, восстановление...')
                    first = False
                download(path + name)
            except Exception as e:
                print(e.__str__())
                return False
    return True


def download(filepath):
    data = requests.get(GIT_CONTENT_URL + filepath)
    byte_writer(filepath, data.content)


def byte_writer(path, byte):
    with open(path, 'wb') as out:
        try:
            out.write(byte)
        finally:
            out.close()
