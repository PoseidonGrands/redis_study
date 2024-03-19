import redis

from redis_db import pool


conn = redis.Redis(connection_pool=pool)

try:
    target_score = 70
    with open('scores.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        for line in lines:
            sid = line.split(',')[0]
            name = line.split(',')[1]
            class_no = line.split(',')[2]
            score_1 = line.split(',')[3]
            score_2 = line.split(',')[4]
            score_3 = line.split(',')[5]

            if int(score_1) >= target_score and int(score_2) >= target_score and int(score_3) >= target_score:
                # 存入redis
                conn.hset(sid, 'name', name)
                conn.hset(sid, 'class_no', class_no)
                conn.hset(sid, 'score_1', score_1)
                conn.hset(sid, 'score_2', score_2)
                conn.hset(sid, 'score_3', score_3)

except Exception as e:
    print(e)
finally:
    del conn


