import requests
from requests.exceptions import ConnectionError
from useragents import *

def get_page(url, option={}):
    """
    抓取代理请求
    :param url:
    :param option:其他参数
    :return:
    """
    print("正在抓取", url)
    try:
        response = requests.get(url, headers=get_user_agent())
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print("抓取失败", url)
        return None




