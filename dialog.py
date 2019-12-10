import database
from utils import get_input


def welcome(conn, addres):
    conn.send(b'Welcome to Safest Russian Army Archive\n')
    while True:
        conn.send(b'\nSelect a menu item to get started with the service\n1. Register\n2. Login\nInput: ')
        data = get_input(conn)
        if data == '1':
            register(conn)
        if data == '2':
            login(conn)


def register(conn):
    conn.send(b'Enter username: ')
    username = get_input(conn)
    conn.send(b'Enter password: ')
    password = get_input(conn)

    success = database.create_user(username, password)
    if success == True:
        conn.send(b'You have been successfully registered\n')
    else:
        conn.send(b'Opps error... Try again\n')


def login(conn):
    conn.send(b'Enter username: ')
    username = get_input(conn)
    conn.send(b'Enter password: ')
    password = get_input(conn)

    result = database.check_password(username, password)
    if result == 1:
        conn.send(b'You have been successfully signed in\n')
        cabinet(conn, username)
    else:
        conn.send(b'Failed to login, check if the username and password are correct\n')


def cabinet(conn, username):
    conn.send("\nHello, {} [{}]!\n".format(username, database.get_rank(username)).encode())
    while(True):
        conn.send(b'\nSelect a menu item to do your dark things\n1. Create private document\n2. List documents\n3. View document\n')
        if username == 'admin':
            conn.send(b'4. Create user\n')
        conn.send(b'Input: ')
        data = get_input(conn)
        if data == '1':
            create_document(conn, username)
        if data == '2':
            list_documents(conn)
        if data == '3':
            view_document(conn, username)
        if data == '4' and username == 'admin':
            create_user(conn)


def create_document(conn, username):
    conn.send(b'Creating document... \n')
    conn.send(b'Enter documents name: ')
    doc_name = get_input(conn)
    conn.send(b'Enter the information you want to save:\n')
    doc_body = get_input(conn)
    rank = database.get_rank(username)
    database.create_document(username, doc_name, doc_body)
    conn.send(b'Your document has been successfully created\n')


def list_documents(conn):
    conn.send(b'Listing documents: \n')
    result = database.list_documents()
    if result == False:
        conn.send(b'There are no documents.\n')
    for document in result:
        conn.send("[{}] {}\n".format(document[0], document[1]).encode("utf-8"))


def view_document(conn, username):
    conn.send(b'Show document... \n')
    conn.send(b'Enter documents id: ')
    doc_id = int(get_input(conn))
    result = database.show_document(username, doc_id)
    if result == False:
        conn.send(b'Za toboi uje viehali, salaga!\n')
    else:
        conn.send("Titte: {}\nAuthor: {}\nBody: {}\n".format(result[2], result[1], result[3]).encode("utf-8"))


def create_user(conn):
    conn.send(b'Enter username: ')
    username = get_input(conn)
    conn.send(b'Enter password: ')
    password = get_input(conn)
    conn.send(b'0. newbie\n1. soldier\n2. sergeant\n3. ensign\n4. lieutenant\n5. captain\n6. major\n7. colonel\n8. brigadier\n9. general\n10. marshal\nChoose rank: ')
    rank = int(get_input(conn))

    success = database.create_user(username, password, rank)
    if success == True:
        conn.send(b'User successfully created\n')
    else:
        conn.send(b'Opps error... Try again\n')
