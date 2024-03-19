import redis
import random

from redis_db import pool


conn = redis.Redis(connection_pool=pool)
roles = ['马云', '丁磊', '张朝阳', '马化腾', '李彦宏']
roles_score = [0 for _ in range(len(roles))]

try:
    # 删除有序集合
    conn.delete('roles')

    # 1、保存结果一次性写入
    for i in range(300):
        # 每个观众给一个人投票
        number = random.randint(0, len(roles) - 1)
        roles_score[number] += 1
    conn.zadd('roles', {roles[0]: roles_score[0],
                        roles[1]: roles_score[1],
                        roles[2]: roles_score[2],
                        roles[3]: roles_score[3],
                        roles[4]: roles_score[4]
                        })

    # 2、投票一次写入一次
    # conn.zadd('roles', {'马云': 0, '丁磊': 0, '张朝阳': 0, '马化腾': 0, '李彦宏': 0})
    # for i in range(300):
    #     # 每个观众给一个人投票
    #     index = random.randint(0, len(roles) - 1)
    #     name = roles[index]
    #     conn.zincrby('roles', 1, name)
    #

    # 提取结果
    res = conn.zrevrange('roles', 0, -1, True)
    print(res)
    for i in res:
        print(i[0].decode('utf-8'), int(i[1]))

    print(roles_score)
except Exception as e:
    print(e)
finally:
    del conn