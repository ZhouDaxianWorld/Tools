# -*- coding:UTF-8 -*-

import requests
import re
import json
import payload
import utils.log as log

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
