import csv

from PyQt5.QtGui import QPalette, QColor


def load_csv():
    with open('Data/Background.csv', 'r') as background:
        rows = [i for i in csv.reader(background, delimiter=';')]
        return rows


def create_palette(window):
    csv_data = load_csv()
    cell = []
    for i in csv_data:
        if i[0] == window:
            cell = i
    r, g, b = (255, 255, 255) if not cell else tuple(map(int, [cell[1], cell[2], cell[3]]))
    f_palette = QPalette()
    f_palette.setColor(QPalette.Background, (QColor(r, g, b)))
    return f_palette
