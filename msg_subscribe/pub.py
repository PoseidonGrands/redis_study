from base import RedisPubSub
"""
这是一个消息发布方
"""


if __name__ == '__main__':
    # 该发布者发布消息的频道是今日播报
    # publisher = RedisPubSub()
    publisher = RedisPubSub(pub='今日播报')
    while 1:
        msg = input('请输入你要发布的消息内容：')
        publisher.public(msg)


