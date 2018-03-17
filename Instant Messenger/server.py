import socket
from threading import Thread
from utils import (obtain_data,
                   send_data,
                   print_data,)


if __name__ == '__main__':
    with socket.socket() as s:
        s.bind(('0.0.0.0', 666))
        s.listen(1)
        connection, ip = s.accept()
        print('ip:{} 已连接'.format(ip))
        t = Thread(target=print_data, args=(connection,))
        t.start()
        while True:
            data = input('')
            if data == '_!exit':
                break
            send_data(data, connection)
        connection.close()
