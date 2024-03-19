import redis

# 一个连接中只能使用定义的逻辑库
try:
    pool = redis.ConnectionPool(
        host='localhost',
        port=6379,
        password='root',
        db=0,
        max_connections=50
    )
except Exception as e:
    print(e)
