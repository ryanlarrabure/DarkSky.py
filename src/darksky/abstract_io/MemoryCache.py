import DateHandler

class MemoryCache(object):

    def __init__(
        self,
        timeout,
        datehandler=None
    ):
        self.__ds = dict()
        self.__datehandler = datehandler or DateHandler.DateHandler()
        self.__timeout = timeout

    def __invalidateCache(self):
        for key, value in [
            item for item in self.__ds.iteritems() if
            item[1]["timestamp"] <= self.__datehandler.currentTime() + 
            item[1]["timeout"]
        ]:
            self.__ds.pop(key)
            


    def insert(self, key, value, timeout=None):
        timeout = timeout or self.__timeout
        self.__invalidateCache()
        timestamp = self.__datehandler.currentTime()
        self.__ds[key] = {
            "value":value,
            "timestamp":timestamp,
            "timeout":self.__datehandler.getTimeDelta(
                seconds=timeout * -1
            )
        }

    def get(self, key):
        self.__invalidateCache()
        if key in self.__ds:
            return self.__ds[key]["value"]
        else:
            raise KeyError("'{}' not in cache".format(key))
