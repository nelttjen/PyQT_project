import csv

from Utils.Pallite import load_csv
from Utils.Values import CSV_DEFAULT


def restore_default_csv(key_id='', is_full_restore=False):
    with open('./Data/Background.csv', 'w', newline='') as out:
        csv_data = load_csv()
        if not csv_data:
            is_full_restore = True
        write = csv.writer(out, delimiter=';')
        if is_full_restore:
            write.writerows(CSV_DEFAULT)
        else:
            try:
                print(csv_data)
                for i, cell in enumerate(CSV_DEFAULT):
                    if cell[0] == key_id:
                        csv_data[i] = cell
                write.writerows(csv_data)
            finally:
                out.close()


def change_color(color, key_id):
    csv_data = load_csv()
    r, g, b = tuple(map(str, color.getRgb()[:-1]))
    for i, cell in enumerate(csv_data):
        if cell[0] == key_id:
            csv_data[i] = [key_id, r, g, b]
    with open('./Data/Background.csv', 'w', newline='') as back_csv:
        try:
            writer = csv.writer(back_csv, delimiter=';')
            writer.writerows(csv_data)
        finally:
            back_csv.close()
