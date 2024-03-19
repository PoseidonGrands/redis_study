from redis_db import pool

import redis
import time


conn = redis.Redis(
    connection_pool=pool
)
conn.set('country', 'UK')
conn.set('city', 'London')
city = conn.get('city').decode('utf-8')
print(city)

conn.expire('city', 4)
time.sleep(5)
city = conn.get('city').decode('utf-8')
print(city)

del conn

