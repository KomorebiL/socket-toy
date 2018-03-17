def obtain_data(connection):
    rs = b''
    while True:
        r = connection.recv(1024)
        rs += r
        if len(r) < 1024:
            break
    return rs.decode('utf-8')


def send_data(data, conn):
    conn.sendall(bytes(data, encoding='utf8'))


def print_data(conn):
    while True:
        data = obtain_data(conn)
        print('你:', data)
