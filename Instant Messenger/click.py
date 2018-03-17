import socket
from threading import Thread
from utils import (obtain_data,
                   send_data,
                   print_data,)


if __name__ == '__main__':
    with socket.socket() as s:
        s.connect(('127.0.0.1', 666))
        t = Thread(target=print_data, args=(s,))
        t.start()
        while True:
            data = input('')
            if data == '_!exit':
                break
            send_data(data, s)
