# -*- coding:UTF-8 -*-

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def getLogger(name):
    logger = logging.getLogger(name)
    return logger