from redis import StrictRedis
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import INITIAL_SCORE, MAX_SCORE, MIN_SCORE
import re
import random
from proxypool.error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化 键值存储数据库
        :param host:
        :param port:
        :param password:
        """
        self.redis = StrictRedis(host=host, port=port, db=0, password=password, decode_responses=True)

    def exists(self, proxy):
        """
        判断有序集合中是否存在代理
        :param proxy:
        :return:
        """
        if not self.redis.zscore(REDIS_KEY, proxy):
            return False
        return True

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，并初始化分数
        :param proxy:
        :param score:
        :return: 添加结果
        """
        if not re.match('\d+.\d+.\d+.\d+\:\d+', proxy):
            print("代理不符合规范要求", proxy)
            return
        if not self.redis.zscore(REDIS_KEY, proxy):
            """
            代理没有分数 也就是没有添加到有序集合
            """
            return self.redis.zadd(REDIS_KEY, score, proxy)

    def batch(self, start, stop):
        """
        批量获取代理
        :param start:开始索引
        :param stop: 结束索引
        :return: 列表
        """
        return self.redis.zrevrange(REDIS_KEY, start, stop-1)

    def all(self):
        """
        获取全部代理
        :return:
        """
        return self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def count(self):
        """
        获取数量
        :return:
        """
        return self.redis.zcount(REDIS_KEY,MIN_SCORE, MAX_SCORE)

    def max(self, proxy):
        """
        如果代理可用，将代理分数设置为最高
        :param proxy:
        :return:
        """
        return self.redis.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def decrease(self, proxy):
        """
        将代理分数减去一分，小于最小值，则删除
        :param proxy:
        :return: 修改后的代理分数
        """
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            return self.redis.zincrby(REDIS_KEY, proxy, -1)
        else:
            return self.redis.zrem(REDIS_KEY, proxy)

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分代理，如果不存在，按照排名获取
        :return: 代理
        """
        result = self.redis.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.redis.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise PoolEmptyError
