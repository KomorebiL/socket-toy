import socket
import select


class ChatRoom(object):
    def __init__(self, ip, port):
        self.ip = {}
        self.names = {}
        self.ip_port = ip, port
        self.inputs = []

    def run(self):
        with socket.socket() as s:
            self.inputs.append(s)
            s.bind(self.ip_port)
            s.listen(5)
            self._select()

    def _select(self):
        while True:
            read, *_ = select.select(self.inputs, [], [])
            self._process(read)

    def _recv(self, connection):
        rs = b''
        while True:
            r = connection.recv(1024)
            rs += r
            if len(r) < 1024:
                break
        data = rs.decode('utf-8')
        if data == '/list':
            self._send_data('当前在线用户列表: {}' .format(list(self.names.values())), connection)
            return None
        return data

    def _process(self, read):
        for s in read:
            if s is self.inputs[0]:
                connection, ip = s.accept()
                string = 'ip:{} 已连接'.format(ip)
                self._send_data_to_clients(string)
                self._send_data('请输入你的名字:', connection)
                self.inputs.append(connection)
                self.ip[connection] = ip
            else:
                try:
                    data = self._recv(s)
                    if data is None:
                        continue
                    if s not in self.names:
                        self.names[s] = data
                        self._send_data('命名成功！你的名字为 {}, 如需获取在线列表，请输入/list，然后回车提交'.format(data), s)
                    else:
                        name = self.names[s]
                        self._send_data_to_clients('{}: {}'.format(name, data))

                except ConnectionResetError:
                    self.inputs.remove(s)
                    ip = self.ip.pop(s)
                    string = 'ip: {}'.format(ip)
                    if s in self.names:
                        name = self.names.pop(s)
                        string += 'name: {}'.format(name)
                    self._send_data_to_clients(string + ' 已离开')

    @staticmethod
    def _send_data(data, client):
        client.sendall(bytes(data, encoding='utf8'))

    def _send_data_to_clients(self, data):
        if len(self.inputs) <= 1:
            return
        for client in self.inputs[1:]:
            self._send_data(data, client)
        print('server:', data)


if __name__ == '__main__':
    server = ChatRoom('0.0.0.0', 666)
    server.run()
