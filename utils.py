import sqlite3

def get_input(conn):
    data = conn.recv(1024)
    return data.decode("utf-8").split("\n")[0]


def sqlquery(sql):
    conn = sqlite3.connect('TopSecret.db')
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    return c.fetchall()