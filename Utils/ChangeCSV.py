import csv

from Utils.Pallite import loadcsv


def restoreDefaultCSV(key_id, isFullRestore=False):
    DEFAULT = [['key_id', 'color_r', 'color_g', 'color_b'],
               ['MainScreen', '229', '228', '226'],
               ['PatternDialog', '220', '220', '220']]
    DATA = loadcsv()
    with open('./Data/Background.csv', 'w', newline='') as out:
        for i, cell in enumerate(DEFAULT):
            if cell[0] == key_id:
                DATA[i] = cell
        write = csv.writer(out, delimiter=';')
        if isFullRestore:
            write.writerows(DEFAULT)
        else:
            write.writerows(DATA)


def changeColor(color, key_id):
    DATA = loadcsv()
    r, g, b = tuple(map(str, color.getRgb()[:-1]))
    for i, cell in enumerate(DATA):
        if cell[0] == key_id:
            DATA[i] = [key_id, r, g, b]
    with open('./Data/Background.csv', 'w', newline='') as back_csv:
        writer = csv.writer(back_csv, delimiter=';')
        writer.writerows(DATA)