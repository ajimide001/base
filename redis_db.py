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
    def get(self, key):
        """
        根据键名获取键值
        :param key:
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

class AccountRedisClient(RedisClient):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,domain='account', name='default', db=0):
        super().__init__(host,port,password,db)
        self.domian = domain
        self.name = name
    def set(self, key, value):
        try:
            return self._db.set(self._key(key),value)
        except:
            raise SetAccountError

    def get(self,key):
        try:
            return self._db.get(self._key(key)).decode('utf-8')
        except:
            raise GetAccountError

    def all(self):
        '''
        获取所有账户，返回字典
        :return:
        '''
        try:
            for key in self._db.keys('{domian}:{name}:*'.format(domian=self.domian,name=self.name)):
                group = key.decode('utf-8').split(':')
                if len(group) == 3:
                    username = group[2]
                    yield {
                        'username':username,
                        'password':self.get(username)
                    }
        except Exception as e:
            print(e.args)
    def delete(self,key):
        try:
            print('删除用户',key)
            return self._db.delete(self._key(key))
        except:
            raise DeleteAccountError

class CookieRedisClient(RedisClient):
    def __init__(self,host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,domain='cookies',name='default',db=0):
        super().__init__(host,password,db)
        self.domain = domain
        self.name = name

    def set(self, key, value):
        try:
            return self._db.set(self._key(key),value)
        except:
            raise SetCookieError
    def get(self,key):
        try:
            return self._db.get(self._key(key)).decode('utf-8')
        except:
            raise GetCookieError

    def get_random(self):
        '''
        随机获取一个cookie
        :return:
        '''
        try:
            keys = self.keys()
            return self._db.get(random.choice(keys))
        except:
            raise GetRandomCookieError
    def all(self):
        '''
        获取所有账号，返回字典
        :return:
        '''
        try:
            for key in self._db.keys('{domain}:{name}:*'.format(domain=self.domain,name=self.name)):
                group = key.decode('utf-8').split(':')
                if len(group) == 3:
                    username = group[2]
                    yield {
                        'username':username,
                        'password':self.get(username)
                    }
        except:
            raise GetAllCookieError
    def delete(self,key):
        try:
            print('删除Cookie:',key)
            return self._db.delete(self._key(key))
        except:
            raise DeleteCookieError
    def count(self):
        """
        获取当前Cookie数目
        :return: 数目
        """
        return len(self.keys())