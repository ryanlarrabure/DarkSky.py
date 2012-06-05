import datetime as datetime_mod
import calendar as calendar_mod

class DateHandler(object):

    def __init__(
        self,
        utcfromtimestamp = None,
        utcnow = None,
        timedelta = None,
        timegm = None
    ):
        self.__utcfromtimestamp = (
            utcfromtimestamp or datetime_mod.datetime.utcfromtimestamp
        )
        self.__utcnow = utcnow or datetime_mod.datetime.utcnow
        self.__timedelta = timedelta or datetime_mod.timedelta
        self.__timegm = timegm or calendar_mod.timegm

    def toDatetime(
        self,
        unixtime
    ):
        return self.__utcfromtimestamp(unixtime)

    def currentTime(self):
        return self.__utcnow()

    def getTimeDelta(self, *args, **kwargs):
        return self.__timedelta(*args, **kwargs)

    def timeTupleToUnix(self, timetuple):
        return self.__timegm(timetuple)
        
