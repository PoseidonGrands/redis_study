import json
import socketserver

from base import RedisPubSub

# 订阅者订阅的频道是今日播报
obj = RedisPubSub(sub='今日播报')
# obj = RedisPubSub(sub='sewell')


class Server(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            # 订阅消息
            _msg = obj.subscribe()

            while 1:
                # 等待获取消息
                msg = _msg.parse_response()

                if msg:
                    # print(f'消息字典是:{msg}')
                    # 把频道名称和消息内容发送给客户端

                    # 巨坑！！！字节数据要存入字典序列化传输得先解码存入字典再进行序列化
                    _data = json.dumps({
                        'channel': msg[1].decode('utf-8'),
                        'data': msg[2].decode('utf-8')
                    })

                    self.request.sendall(_data.encode('utf-8'))


        except Exception as e:
            print(self.client_address, 'close', f'except:{e}')


    def setup(self):
        """客户端连接会触发的函数"""
        print(f'客户端：{self.client_address}')

    def finish(self):
        print('finish')


if __name__ == '__main__':
    host, port = 'localhost', 8888
    server = socketserver.TCPServer((host, port), Server)
    server.serve_forever()