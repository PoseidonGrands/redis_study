import redis

from redis_db import pool


conn = redis.Redis(connection_pool=pool)
pipline = None

try:
    # 字符串操作
    conn.delete('country', 'city')
    conn.mset({'country': 'UK', 'city': 'London'})
    result = conn.mget('country', 'city')
    for i in result:
        print(i.decode('utf-8'))

    print('------')

    # 列表操作
    conn.rpush('dname', 'one', 'two', 'three', 'four')
    conn.lpop('dname')
    result = conn.lrange('dname', 0, -1)
    for i in result:
        print(i.decode('utf-8'))

    print('------')

    # 集合操作
    conn.sadd('employee', 200, 300, 400, 500)
    conn.srem('employee', 300)
    result = conn.smembers('employee')
    for i in result:
        print(i.decode('utf-8'))

    print('------')

    # 有序集合操作
    conn.zadd('keywords', {'马云': 0, '张朝阳': 0, '马化腾': 0})
    conn.zincrby('keywords', 10, '马化腾')
    result = conn.zrevrange('keywords', 0, -1)
    print(conn.zcard('keywords'))
    for i in result:
        print(i.decode('utf-8'))

    print('------')

    # 哈希操作
    conn.hset('2000', 'name', 'sewell')
    conn.hset('2000', 'age', '24')
    conn.hset('2000', 'hobby', 'swim')
    conn.hdel('2000', 'hobby')
    is_exist = conn.hexists('2000', 'name')
    print(is_exist)
    result = conn.hgetall('2000')
    for key, value in result.items():
        print(key.decode('utf-8'), value.decode('utf-8'))

    # 事务操作
    pipline = conn.pipeline()
    pipline.watch('2000')
    pipline.multi()
    pipline.hset('2000', 'age', '18')
    pipline.execute()
except Exception as e:
    print(e)
finally:
    del conn
    if 'pipline' in dir():
        pipline.reset()
