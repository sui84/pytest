#encoding=utf-8
import redis

class RedisHelper(object):
    def __init__(self, server='localhost',port=6379):
        self.r=redis.Redis(host='127.0.0.1',port=6379)
