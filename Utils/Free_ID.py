import sqlite3


def get_free_id():
    database = sqlite3.connect('./Data/patterns.db')
    cursor = database.cursor()
    res = cursor.execute("""SELECT id FROM p_custom WHERE isUsed = 0""").fetchone()
    database.close()
    return res[0]
