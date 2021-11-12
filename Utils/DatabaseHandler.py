import sqlite3

from Utils.Path import *
from Utils.Values import NEW_PATTERN_PATH, DEFAULT_PATTERNS_COUNT


def change_to_db(pattern: list):
    database = sqlite3.connect('./Data/patterns.db')
    cursor = database.cursor()
    try:
        offset = 0 if pattern[5] else DEFAULT_PATTERNS_COUNT
        if pattern[0] != NEW_PATTERN_PATH:
            p_id = int(get_clean_id(pattern[0])) - offset
        else:
            p_id = pattern[6]

        text1_enabled, text1_xy, text1_size, text1_text_size, text1_delimiter, text1_align = pattern[1]
        text2_enabled, text2_xy, text2_size, text2_text_size, text2_delimiter, text2_align = pattern[2]
        image1_enabled, image1_xy, image1_size = pattern[3]
        image2_enabled, image2_xy, image2_size = pattern[4]
        table = 'p_default' if pattern[5] else 'p_custom'
        res = f'''
        UPDATE {table} 
        SET {'isUsed = 1,' if not pattern[5] else ''}
        line1 = {1 if text1_enabled else 'NULL'},
        line2 = {1 if text2_enabled else 'NULL'},
        image1 = {1 if image1_enabled else 'NULL'},
        image2 = {1 if image2_enabled else 'NULL'},
        line1Size = {f'"{text1_size[0]}x{text1_size[1]}"' if text1_size else 'NULL'},
        line1XY = {f'"{text1_xy[0]}x{text1_xy[1]}"' if text1_xy else 'NULL'},
        line1Delimiter = {text1_delimiter if text1_delimiter else 'NULL'},
        text1Size = {text1_text_size if text1_text_size else 'NULL'},
        text1Align = {f'"{text1_align}"' if text1_align else 'NULL'},
        line2Size = {f'"{text2_size[0]}x{text2_size[1]}"' if text2_size else 'NULL'},
        line2XY = {f'"{text2_xy[0]}x{text2_xy[1]}"' if text2_xy else 'NULL'},
        line2Delimiter = {text2_delimiter if text2_delimiter else 'NULL'},
        text2Size = {text2_text_size if text2_text_size else 'NULL'},
        text2Align = {f'"{text2_align}"' if text2_align else 'NULL'},
        image1Size = {f'"{image1_size[0]}x{image1_size[1]}"' if image1_size else 'NULL'},
        image1XY = {f'"{image1_xy[0]}x{image1_xy[1]}"' if image1_xy else 'NULL'},
        image2Size = {f'"{image2_size[0]}x{image2_size[1]}"' if image2_size else 'NULL'},
        image2XY = {f'"{image2_xy[0]}x{image2_xy[1]}"' if image2_xy else 'NULL'}
        WHERE id = {p_id}
        '''
        cursor.execute(res)
        database.commit()
    finally:
        # в любом случае закроем коннект к базе
        database.close()


def remove_pattern_from_db(p_id):
    database = sqlite3.connect('./Data/patterns.db')
    cursor = database.cursor()
    try:
        res = f'''
        UPDATE p_custom
        SET isUsed = 0,
        line1 = NULL,
        line2 = NULL,
        image1 = NULL,
        image2 = NULL,
        line1Size = NULL,
        line1XY = NULL,
        line1Delimiter = NULL,
        text1Size = NULL,
        text1Align = NULL,
        line2Size = NULL,
        line2XY = NULL,
        line2Delimiter = NULL,
        text2Size = NULL,
        text2Align = NULL,
        image1Size = NULL,
        image1XY = NULL,
        image2Size = NULL,
        image2XY = NULL
        WHERE id = {int(p_id) - DEFAULT_PATTERNS_COUNT}
        '''
        cursor.execute(res)
        database.commit()
    finally:
        # в любом случае закроем коннект к базе
        database.close()
