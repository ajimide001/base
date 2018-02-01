#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random
import redis
from error import *
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWORD = ''
REDIS_DOMAIN = ''
REDIS_NAME = ''
class RedisClient(object):
    def __init__(self,host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWORD,db=0):
        """
        初始化Redis连接
        :param host:地址
        :param port:端口
        :param password:密码
        :param db:
        """
        if password:
            self._db = redis.Redis(host=host, port=port, password=password,db=db)
        else:
            self_db = redis.Redis(host=host,port=port)
        self.domain = REDIS_DOMAIN
        self.name = REDIS_NAME

    def _key(self, key):
        """
        得到格式化的key
        :param key: 最后一个参数key
        :return:
        """
        return "{domain}:{name}:{key}".format(domain=self.domain, name=self.name, key=key)

    def set(self,key,value):
        """
        设置键值对
        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError
    def delete(self,key):
        """
        根据键名删除键值对
        :param key:
        :return:
        """
        raise NotImplementedError
    def keys(self):
        """
        得到所有的键名
        :return:
        """
        return self._db.keys('{domian}:{name}:*'.format(domian=self.domain, name=self,name))
    def flush(self):
        """
        清空数据库。慎用
        :return:
        """
        self._db.flushall()