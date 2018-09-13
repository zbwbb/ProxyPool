import aiohttp
from proxypool.db import RedisClient
from proxypool.setting import TEST_URL, VALID_STATUS_CODES, BATCH_TEST_SIZE

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

import asyncio
import time



class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        异步测试单个代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                """
                在Python3以后，字符串和bytes类型彻底分开了。字符串是以字符为单位进行处理的，bytes类型是以字节为单位处理的。
                直接以默认的utf-8编码解码bytes成string
                """
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print("正在测试", proxy)
                async with session.get(TEST_URL, allow_redirects=False, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        # 将代理设置为分数最大
                        self.redis.max(proxy)
                        print("代理", proxy, '可用, 设置为100')
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法', response.status, 'IP', proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                print("代理验证失败", proxy)
                self.redis.decrease(proxy)

    def run(self):
        """
        测试函数
        :return:
        """
        print('测试器开始运行')
        try:
            count = self.redis.count()
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                """获取测试代理"""
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print("测试器发生错误", e.args)


