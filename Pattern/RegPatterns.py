import sqlite3

from Pattern.Pattern import Pattern
from Utils.Values import DEFAULT_PATTERNS_COUNT


def reg_new_pattern(res: list, isDefault=True):
    path = './Images/Patterns'
    pattern_id = f'pattern{res[0] if isDefault else res[0] + DEFAULT_PATTERNS_COUNT}'
    pattern = Pattern(line1=res[1], line2=res[2],
                      image1=res[3], image2=res[4],
                      line1Size=tuple(map(int, res[5].split('x'))) if res[5] else res[5],
                      line1XY=tuple(map(int, res[6].split('x'))) if res[6] else res[6],
                      text1Delimiter=res[7] if res[7] else 0,
                      text1Size=res[8] if res[8] else 0,
                      text1Align=res[9] if res[9] else 'center',
                      line2Size=tuple(map(int, res[10].split('x'))) if res[10] else res[10],
                      line2XY=tuple(map(int, res[11].split('x'))) if res[11] else res[11],
                      text2Delimiter=res[12] if res[12] else 0,
                      text2Size=res[13] if res[13] else 0,
                      text2Align=res[14] if res[14] else 'center',
                      image1Size=tuple(map(int, res[15].split('x'))) if res[15] else res[15],
                      image1XY=tuple(map(int, res[16].split('x'))) if res[16] else res[16],
                      image2Size=tuple(map(int, res[17].split('x'))) if res[17] else res[17],
                      image2XY=tuple(map(int, res[18].split('x'))) if res[18] else res[18],
                      filePath=f'{path}/{pattern_id}.png', default=isDefault
                      )
    return pattern


def create_default(patterns: list):
    database = sqlite3.connect('./Data/patterns.db')
    cursor = database.cursor()
    for i in range(11):
        res = cursor.execute(f"""SELECT *
                                FROM p_default
                                WHERE id == {i + 1}""").fetchone()
        pattern = reg_new_pattern(res, True)
        patterns.append(pattern)
    database.close()


def create_custom(patterns: list):
    database = sqlite3.connect('./Data/patterns.db')
    cursor = database.cursor()
    res = f"""SELECT *
            FROM p_custom
            WHERE isUsed = 1
        """
    result = cursor.execute(res).fetchall()
    for i in range(len(result)):
        res_list = list(result[i])
        del res_list[1]
        result[i] = res_list
    for i in range(len(result)):
        pattern = reg_new_pattern(result[i], False)
        patterns.append(pattern)
    database.close()


def recreate_patterns():
    patterns = []
    create_default(patterns)
    create_custom(patterns)
    return patterns
