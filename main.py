import redis

#
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    password='root',
    db=0,
    max_connections=20
)

