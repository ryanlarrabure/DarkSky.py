import redis as redis_mod

class RedisCache(object):
    
    def __init__(
        self,
        strict_redis=None,
        redis=redis_mod,
        password=None,
        hostname=None,
        db=None,
        port=None
    ):
        redis_args = {}
        if password: redis_args["password"] = password
        if hostname: redis_args["hostname"] = hostname
        if db: redis_args["db"] = db
        if port: redis_args["port"] = port
        self.__strict_redis = strict_redis or redis.StrictRedis(**redis_args)
        

    def insert(
        self,
        key,
        value,
        timeout=None
    ):
        self.__strict_redis.set(key, value)
        if timeout:
            self.__strict_redis.expire(key, timeout)

    def get(
        self,
        key
    ):
        ret = self.__strict_redis.get(key)
        if not ret:
            raise KeyError("Redis doesn't have key '{}'".format(key))
        return ret
