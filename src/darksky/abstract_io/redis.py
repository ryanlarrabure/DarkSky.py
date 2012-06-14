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
        

    def set(
        self,
        key,
        value
    ):
        self.__strict_redis.set(key, value)

    def get(
        self,
        key
    ):
        return self.__strict_redis.get(key)
