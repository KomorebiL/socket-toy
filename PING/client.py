import socket
import struct
import time


TYPE = [0x08]
BE_LE = [0x00] * 2
DATA = [0x68, 0x65, 0x6c, 0x6c, 0x6f]


class Client(object):
    def __init__(self, ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        self.s.settimeout(1)
        self.ip = (ip, 1)

    @staticmethod
    def _checksum(data):
        sum = 0
        for d in data:
            sum += d
        hex_sum = hex(sum)
        if len(hex_sum) > 6:
            return [~(int(hex_sum[:3], 16) + int(hex_sum[3:], 16)) & 0xffff]
        else:
            return [~sum & 0xffff]

    def ping(self):
        _data = TYPE + BE_LE + DATA
        data = struct.pack('9H', *(TYPE + self._checksum(_data) + BE_LE + DATA))

        start_time = time.time()
        self.s.sendto(data, self.ip)
        try:
            self.s.recvfrom(1024)
        except socket.timeout:
            print('请求超时')
        else:
            time_ms = (time.time() - start_time) * 1000
            print('{:.1f} ms'.format(time_ms))
            return time_ms

if __name__ == '__main__':
    client = Client('180.149.134.141')
    result = []
    for i in range(4):
        result.append(client.ping())
    if None not in result:
        print('平均:{:.1f} ms'.format(sum(result) / len(result)))

