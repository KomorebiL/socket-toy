import socket
import select
from threading import Thread


class Client(object):
    def __init__(self, ip, port):
        self.ip_port = ip, port

    def _print_data(self, s):
        while True:
            read, *_ = select.select([s], [], [])
            self._process(read)

    def _process(self, read):
        for s in read:
            data = self._recv(s)
            if len(data) == 0:
                print('服务器断开连接!')
                exit(0)
            else:
                print(data)

    @staticmethod
    def _recv(s):
        rs = b''
        while True:
            r = s.recv(1024)
            rs += r
            if len(r) < 1024:
                break
        return rs.decode('utf-8')

    def _print(self, s):
        t = Thread(target=self._print_data, args=(s,))
        t.start()

    @staticmethod
    def _send_data(data, conn):
        conn.sendall(bytes(data, encoding='utf8'))

    def _input(self, s):
        while True:
            data = input('')
            self._send_data(data, s)

    def run(self):
        with socket.socket() as s:
            s.connect(self.ip_port)
            self._print(s)
            self._input(s)


if __name__ == '__main__':
    client = Client('127.0.0.1', 666)
    client.run()
