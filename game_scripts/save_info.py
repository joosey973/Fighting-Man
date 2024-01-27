import sqlite3


def get_info(request="", values="", type_of_request="get"):
    connection = sqlite3.connect("files/info.db")
    curs = connection.cursor()
    if type_of_request == "get":
        res = curs.execute(request).fetchall()[0][0]
        connection.close()
        return res
    else:
        curs.execute(request.format(values))
        connection.commit()
        connection.close()
        return


def insert_info():
    connection = sqlite3.connect("files/info.db")
    curs = connection.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS game_info
                    (Resolution TEXT UNIQUE, Level INT)''')
    curs.execute('''INSERT INTO game_info(Resolution, Level)
                            VALUES(?, ?)''', ("800, 600", 1))
    connection.commit()
    connection.close()
