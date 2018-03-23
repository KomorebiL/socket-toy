import socket
import struct
import time


DATA = [0x0800, 0xf7ff] + [0x0000] * 68


class Client(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.s.settimeout(1)
        self.time_to_live = 1
        self.data = struct.pack('!70H', *DATA)

    def _send(self, ip):
        self.s.setsockopt(socket.SOL_IP, socket.IP_TTL, self.time_to_live)
        self.s.sendto(self.data, (ip, 1))
        self.time_to_live += 1

    def _recv(self):
        data, ip_port = self.s.recvfrom(1024)
        return data, ip_port[0]

    def run(self, ip):
        while True:
            start_time = time.time()
            self._send(ip)
            try:
                data, recv_ip = self._recv()
            except socket.timeout:
                print('请求超时')
            else:
                print('{:>4.1f} ms     ip: {}'.format((time.time() - start_time) * 1000, recv_ip))
                if data[20:][0] == 0x00:
                    break

if __name__ == '__main__':
    client = Client()
    client.run('14.215.177.38')