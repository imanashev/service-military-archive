from utils import sqlquery


def init_db():
    sqlquery("CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        "username text NOT NULL UNIQUE, " 
        "password text NOT NULL, "
        "rank integer NOT NULL)")
    sqlquery("CREATE TABLE IF NOT EXISTS documents "
        "(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        "author text, " 
        "title text, "
        "body text)")


def create_user(username, password, rank=0):
    if len(username) < 3 or len(password) < 3 or rank < 0 or rank > 10:
        return False

    result = sqlquery("SELECT * FROM users WHERE username='{}'".format(username))
    if len(result) == 0:
        result = sqlquery("INSERT INTO users (username, password, rank) VALUES ('{}', '{}', '{}')".format(username, password, rank))
    return len(result) == 0


def check_password(username, password):
    if len(username) < 3 or len(password) < 3:
        return False
    result = sqlquery("SELECT password FROM users WHERE username='{}'".format(username))
    if len(result) == 0:
        return False
    stored_password = result[0][0]
    return password == stored_password


def get_rank(username):
    result = sqlquery("SELECT rank FROM users WHERE username='{}'".format(username))
    if len(result) == 0:
        return 0
    return result[0][0]


def create_document(username, doc_name, doc_body):
    result = sqlquery("INSERT INTO documents (author, title, body) VALUES ('{}', '{}', '{}')".format(username, doc_name, doc_body))
    return len(result) == 0


def list_documents():
    result = sqlquery("SELECT id, title FROM documents")
    if len(result) == 0:
            return False
    return result


def show_document(username, doc_id):
    # можно реализовать проверку доступности документа во внешней библиотеке (как изначально и задумывалось)
    result = sqlquery("SELECT * FROM documents WHERE id='{}'".format(doc_id))
    if len(result) != 0:
        user_rank = get_rank(username)
        author = result[0][1]
        author_rank = get_rank(author)
        if (user_rank > author_rank) or (username == author):
            return result[0]
    return False
