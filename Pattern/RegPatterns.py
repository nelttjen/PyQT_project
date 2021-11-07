import sqlite3

from Pattern.Pattern import Pattern


def create_default(patterns: list):
    path = './Images/Patterns'
    database = sqlite3.connect('./Data/patterns.db')
    cursor = database.cursor()
    for i in range(11):
        res = cursor.execute(f"""SELECT 
       id,
       line1,
       line2,
       image1,
       image2,
       line1Size,
       line1XY,
       line1Delimiter,
       text1Size,
       text1Align,
       line2Size,
       line2XY,
       line2Delinmiter,
       text2Size,
       text2Align,
       image1Size,
       image1XY,
       image2Size,
       image2XY
                                FROM p_default
                                WHERE id == {i + 1}""").fetchone()
        pattern_id = f'pattern{res[0]}'
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
                          filePath=f'{path}/{pattern_id}.png', default=True
                          )
        patterns.append(pattern)
    database.close()


def create_custom(patterns: list):
    pass


def recreate_patterns():
    patterns = []
    create_default(patterns)
    create_custom(patterns)
    return patterns
