import csv

from Utils.Pallite import load_csv


def restore_default_csv(key_id, isFullRestore=False):
    default = [['key_id', 'color_r', 'color_g', 'color_b'],
               ['MainScreen', '229', '228', '226'],
               ['PatternDialog', '220', '220', '220']]
    csv_data = load_csv()
    with open('./Data/Background.csv', 'w', newline='') as out:
        for i, cell in enumerate(default):
            if cell[0] == key_id:
                csv_data[i] = cell
        write = csv.writer(out, delimiter=';')
        if isFullRestore:
            write.writerows(default)
        else:
            write.writerows(csv_data)


def change_color(color, key_id):
    csv_data = load_csv()
    r, g, b = tuple(map(str, color.getRgb()[:-1]))
    for i, cell in enumerate(csv_data):
        if cell[0] == key_id:
            csv_data[i] = [key_id, r, g, b]
    with open('./Data/Background.csv', 'w', newline='') as back_csv:
        writer = csv.writer(back_csv, delimiter=';')
        writer.writerows(csv_data)
