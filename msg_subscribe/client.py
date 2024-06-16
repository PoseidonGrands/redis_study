import json
import socket


def work():
    client = socket.socket()

    client.connect(('localhost', 8888))

    while 1:
        msg = client.recv(1024)
        # 接收到消息才输出
        if msg:
            data = json.loads(msg.decode('utf-8'))
            print(f'channel:{data.get("channel")}，msg:{data.get("data")}')



if __name__ == '__main__':
    work()