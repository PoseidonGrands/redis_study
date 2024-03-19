import redis
import random

from redis_db import pool
from concurrent.futures import ThreadPoolExecutor


def buy(uid):
    """
    秒杀结束情况：
    1、已经过了抢购时间
    2、秒杀人数已经等于可抢购人数
    """
    conn_buy = redis.Redis(connection_pool=pool)
    pipeline = conn_buy.pipeline()
    try:
        # 检查秒杀是否有效(记录超时被删除则代表秒杀时间已过
        if conn_buy.exists('kill_flag') == 1:
            pipeline.watch('kill_num', 'kill_user')
            kill_total = int(pipeline.get('kill_total').decode('utf-8'))
            kill_num = int(pipeline.get('kill_num').decode('utf-8'))
            # 还可秒杀
            if kill_num < kill_total:
                pipeline.multi()
                pipeline.incr('kill_num')
                pipeline.rpush('kill_user', uid)
                pipeline.execute()
            else:
                return '秒杀已结束'
    except Exception as e2:
        print(e2)
    finally:
        if 'pipeline' in dir():
            pipeline.reset()
        del conn_buy


if __name__ == '__main__':
    # 生成用户列表
    user_set = set()
    while True:
        _uid = random.randint(10000, 100000)
        user_set.add(_uid)

        if len(user_set) == 1000:
            break

    # 创建redis连接对象
    conn = redis.Redis(connection_pool=pool)
    try:
        conn.delete('kill_total', 'kill_num', 'kill_flag', 'kill_user')
        conn.set('kill_total', 50)
        conn.set('kill_num', 0)
        conn.set('kill_flag', 1)
        conn.expire('kill_flag', 60)
    except Exception as e:
        print(e)
    finally:
        del conn

    # 创建线程池(1000人参与秒杀，但是因为网络、设备等原因同一个时间只有一部分人参与秒杀
    t = ThreadPoolExecutor(40)
    # 随机一个用户
    for _ in range(len(user_set)):
        t.submit(buy, user_set.pop())


"""
解释1：
如果两个用户同时尝试进行秒杀，而此时秒杀数仍然足够（例如剩余10个），并且它们同时监视相同的键，并且在事务执行期间没有其他操作改变了这些键，那么它们两个提交事务的操作都应该成功。
因为在 Redis 中，事务是按照先后顺序执行的，并且在 WATCH 的情况下，如果被监视的键在事务执行期间没有发生变化，那么所有事务都会被顺利执行。

解释2：
watch 命令用于在执行事务前监视一个或多个键，如果在执行 multi 命令之后，直到执行 exec 命令之前，被监视的键被其他客户端改变（包括当前客户端），那么事务将被打断。这种机制保证了如果监视的数据被修改，事务不会执行，从而实现了乐观锁的效果。

在你的例子中，用户a和用户b同时 watch 到 kill_num（假设为40）时，假设用户a先执行了事务，即他们成功地将 kill_num 从40增加到了41，并且成功地将自己的uid加入到了 kill_user 列表中。

当用户b尝试提交他们的事务时，由于 kill_num 已经被用户a改变（从40变成了41），用户b监视的 kill_num 的值已经不是最新的了。这时，用户b的事务会因为 watch 设置的条件（即 kill_num 在事务执行过程中被修改）不满足而被打断，他们的事务不会被成功执行。

因此，即使理论上还有足够的秒杀数量让用户b秒杀成功，由于 Redis 事务的乐观锁特性，用户b的秒杀操作在这种竞争条件下不会成功。这就需要用户b重新尝试整个秒杀操作，希望在下一次能够在没有其他用户修改 kill_num 的情况下完成事务。

总的来说，这种机制保证了在高并发场景下秒杀的公平性和一致性，避免了超卖的问题。

"""