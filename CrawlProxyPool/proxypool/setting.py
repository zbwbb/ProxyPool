# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = '6379'

# Redis密码，如无填 None
REDIS_PASSWORD = None

# 有序集合的名字
REDIS_KEY = 'proxies'

# 代理分数
INITIAL_SCORE = 10
MAX_SCORE = 100
MIN_SCORE = 0

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 测试的URL
TEST_URL = 'http://www.baidu.com'

# 测试的状态码
VALID_STATUS_CODES = [200, 302]

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 步长
BATCH_TEST_SIZE = 10

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True