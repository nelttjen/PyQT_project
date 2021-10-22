import json

from PyQt5.QtGui import QPalette, QColor


def loadJson():
    with open('Json/Background.json', 'r') as background:
        return json.load(background)


def createPallite(window):
    DATA = loadJson()
    f_palette = QPalette()
    f_palette.setColor(QPalette.Background, (QColor(int(DATA[window]['r']),
                                                    int(DATA[window]['g']),
                                                    int(DATA[window]['b']))))
    return f_palette