# -*- coding:UTF-8 -*-

import requests
import re
import json
import payload
import utils.log as log

"""
根据经验所得，可以测试以下几种payload：
1. 无任何转码的payload
2. 使用url编码转换的payload
3. 使用两次url编码的payload
4. 对于href="可控变量"可使用unicode字符的payload
"""
logger = log.getLogger(__name__)

def xssFuzz(url, method, params, data, headers, timeout=30):
    method = method.upper()

    for payLoad in payload.payLoadList:
        for key, value in params.items():
            params[key] = payLoad
        for key, value in data.items():
            data[key] = payLoad

        response = requests.request(method, url, params=params, data=data, headers=headers, timeout=timeout, allow_redirects=True)
        text = re.sub(r"\r", "", response.text)
        text = re.sub(r"\n", "", text)

        if payLoad in text:
            logger.info("xss模糊测试，成功，payload：%s", payLoad)
        else:
            logger.info("xss模糊测试，失败，payload：%s", payLoad)

if __name__ == "__main__":
    url = "http://www.aitugu.com/search.html"
    method = "get"
    params = {"q": "1", "test": 2}
    data = {}
    headers = {}
    xssFuzz(url, method, params, data, headers)
