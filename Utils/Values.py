DEFAULT_PATTERNS_COUNT: int = 11
CREATE: int = 0
CHANGE: int = 1
CHANGE_DEFAULT: int = 2
INFO_SIZE: str = 'Текущий размер:\n'
INFO_POSITION: str = 'Текущее положение:\n'
NEW_PATTERN_PATH: str = './Images/Temp/new_pattern.png'
GRID_PATTERN_SIZE: tuple = (284, 190)

DEFAULT_PATH: str = './Images/Default/default.png'
OUTPUT_PATH: str = './Images/Output/output.png'
PREVIEW_PATH: str = './Images/Preview/preview.png'
PREVIEW_SIZE: tuple = (854, 540)

CSV_DEFAULT: list = [['key_id', 'color_r', 'color_g', 'color_b'],
                     ['MainScreen', '229', '228', '226'],
                     ['PatternDialog', '220', '220', '220']]

CSS_DEFAULT = '''
QPushButton {
    border-color: black;
    border-style: solid;
    border-width: 1px;
    background-color: white;
}
QPushButton:hover {
    background-color: #bbcbcf;\
}
QPushButton:disabled {
    border-color: #aebec2;
    border-style: solid;
    border-width: 1px;
    background-color: white;
}
'''[1:]

GIT_CONTENT_URL = 'https://raw.githubusercontent.com/nelttjen/PyQT_project/main/'
