#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 2023-08-04 11:17

import os
import logging
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s [%(funcName)s: %(filename)s,%(lineno)d] - %(levelname)s : %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_PATH = "log/"

# 初始化日志文件配置
def initLog(fileName,logger):
    # 创建日志文件夹
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    myapp = logging.getLogger(logger)
    myapp.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(LOG_PATH+fileName, maxBytes=128*1024, backupCount=60)
    handler.setFormatter(logging.Formatter(LOG_FORMAT,DATE_FORMAT))
    myapp.addHandler(handler)
    return myapp