import redis

class RedisPubSub(object):
    def __init__(self,
                 host='localhost',
                 port='6379',
                 db=1,
                 password='root',
                 pub='sewell',
                 sub='sewell'):
        pool = redis.ConnectionPool(host=host,
                                    port=port,
                                    db=db,
                                    password=password)

        self.conn = redis.StrictRedis(connection_pool=pool)

        # 消息发布者发布的频道
        self.pub = pub
        # 消息订阅者订阅的频道
        self.sub = sub
        self._sub = None

    def public(self, msg):
        """消息发布"""
        # 存在频道
        if self.pub:
            # 消息发布者使用pub这个频道发布消息
            self.conn.publish(self.pub, msg)
            return True
        else:
            return False

    def subscribe(self):
        """消息订阅"""
        if self.pub:
            # 订阅对象，专门用来处理 Redis 的发布/订阅操作
            self._sub = self.conn.pubsub()
            # 实际订阅频道
            self._sub.subscribe(self.sub)
            # 解析从订阅的通道（频道）接收到的响应
            self._sub.parse_response()

            return self._sub



