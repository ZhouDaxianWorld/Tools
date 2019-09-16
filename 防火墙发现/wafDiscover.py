# -*- coding:UTF-8 -*-

import requests
import json
import re
import utils.log as log

logger = log.getLogger(__name__)

def wafDiscern(url, method, params, data, timeout=30):
    method = method.upper()

    with open("./wafFeature.json", 'rb') as f:
        wafFeatureList = json.load(f)

    # 按照原始的提交的方法，参数，数据 进行请求，用最接近的方法进行测试。
    params['xss'] = "<script>alert(xss)</script>"
    data['xss'] = "<script>alert(xss)</script>"

    response = requests.request(method, url, params=params, data=data, timeout=timeout, allow_redirects=True)
    text = re.sub(r"\r", "", response.text)
    text = re.sub(r"\n", "", text)
    headers = str(response.headers)
    logger.debug(response.status_code)
    logger.debug(response.headers)

    wafDiscernResult = []
    wafDiscernResult.append(("可能存在防火墙", 0))
    if response.status_code > 400:
        for wafName, wafFeature in wafFeatureList.items():
            score = 0
            if re.search(wafFeature['page_pattern'], text, re.I):
                score += 1
            if response.status_code == wafFeature['status_code']:
                score += 0.5
            if re.search(wafFeature['headers_pattern'], headers, re.I):
                score += 1
                wafDiscernResult.append((wafName, score))

    wafDiscernResult = sorted(wafDiscernResult, key=lambda k:k[1], reverse=True)
    return wafDiscernResult[0]

if __name__ == "__main__":
    wafDiscernResult = wafDiscern("http://www.wbiao.cn", "GET", {}, {}, timeout=10)
    print(wafDiscernResult)