import datetime as datetime_mod

class DateHandler(object):

    def __init__(
        self,
        utcfromtimestamp = None,
        utcnow = None,
        timedelta = None
    ):
        self.__utcfromtimestamp = (
            utcfromtimestamp or datetime_mod.datetime.utcfromtimestamp
        )
        self.__utcnow = utcnow or datetime_mod.datetime.utcnow
        self.__timedelta = timedelta or datetime_mod.timedelta

    def toDatetime(
        self,
        unixtime
    ):
        return self.__utcfromtimestamp(unixtime)

    def currentTime(self):
        return self.__utcnow()

    def getTimeDelta(self, *args, **kwargs):
        return self.__timedelta(*args, **kwargs)
