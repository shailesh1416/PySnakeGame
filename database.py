import sqlite3


def getLevel(id):

    # Connecting to sqlite3
    conn = sqlite3.connect('game')

    # Creating cursor object 
    cursor = conn.cursor()

    # Retriving data
    query = f'SELECT * FROM level where id={id}'
    cursor.execute(query)

    # levels = cursor.fetchall()


    # for level in levels:
    #     print('->',level)


    level = cursor.fetchone()
    conn.commit()
    conn.close()
    return level

# level = getLevel(id)
