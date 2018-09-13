from proxypool.crawler import Crawler
from proxypool.db import RedisClient
from proxypool.setting import POOL_UPPER_THRESHOLD

class GetterProxy(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        :return:
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("获取器开始执行")
        if not self.is_over_threshold():
            for callback_index in range(Crawler.__CrawlFuncCount__):
                # 获取方法
                callback = self.crawler.__CrawlFunc__[callback_index]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                # 添加代理
                for proxy in proxies:
                    self.redis.add(proxy)

