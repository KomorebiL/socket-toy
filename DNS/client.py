import socket
import struct
import random


FLAGS = ['01', '00']
QUESTIONS = ['00', '01']
RR = ['00'] * 6
END = ['00', '01', '00', '01']


class Client(object):
    def __init__(self, ip, port):
        self.ip_port = ip, port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _send(self, url):
        data = self.encode(self.new_transaction() + FLAGS + QUESTIONS + RR + self.hex_url(url) + END)
        self.socket.sendto(data, self.ip_port)

    def _recv(self):
        data, _ = self.socket.recvfrom(1024)
        return self.decode(data)

    @staticmethod
    def encode(data):
        string = b''
        for d in data:
            d_ = int(d, 16)
            string += struct.pack('B', d_)
        return string

    def decode(self, data):
        data = data[12:]
        data = data[self._get_url_index(data) + 5 + 10:]
        data_length = int(data[:2][1])
        return '.'.join([str(s) for s in data[2: 2 + data_length]])

    @staticmethod
    def _get_url_index(data):
        index = 0
        while True:
            if data[index] == 0:
                break
            index += data[index] + 1
        return index

    @staticmethod
    def hex_url(url):
        data = []
        url_split = url.split('.')
        for string in url_split:
            data.append('0{}'.format(len(string)))
            for s in string:
                data.append(hex(ord(s))[2:])
        data.append('00')
        return data

    @staticmethod
    def new_transaction():
        return [str(random.randint(10, 100)), str(random.randint(10, 100))]

    def run(self, url):
        self._send(url)
        print(self._recv())


if __name__ == '__main__':
    client = Client('114.114.114.114', 53)
    client.run('www.qq.com')
