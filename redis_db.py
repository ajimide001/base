#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random
import redis

class RedisClient(object):
    def __init__(self,host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWORD,db=0):
        """
        初始化Redis连接
        :param host:地址
        :param port:端口
        :param password:密码
        :param db:
        """