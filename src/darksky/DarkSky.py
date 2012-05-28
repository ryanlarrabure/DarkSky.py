import json
from abstract_io import HTTP, DateHandler

class DarkSkyResponse(object):
    def __init__(
        self,
        response_body,
        forecast_type,
        datehandler = None
    ):
        self.__response_body = response_body
        self.forecast_type = forecast_type
        self.__datehandler = datehandler or DateHandler()
        self.__setCurrentTime()
        self.__setProperties()

    def __setCurrentTime(self):
        self.__instantiation_time = self.__datehandler.currentTime()

    def __setTimes(self):
        if "hourPrecipitation" in dir(self):
            for entry in self.hourPrecipitation:
                entry["time"] = self.__datehandler.toDatetime(entry["time"])
        if "dayPrecipitation" in dir(self):
            for entry in self.dayPrecipitation:
                entry["time"] = self.__datehandler.toDatetime(entry["time"])

    def  __setProperties(self):
        exclusions = ['hourSummary']
        for prop in self.__response_body.keys():
            if prop not in exclusions:
                self.__setattr__(prop, self.__response_body[prop])
        self.__setTimes() 

    @property
    def hourSummary(self):
        time_field = ""
        if self.__datehandler.currentTime() >= self.getTimeToChange():
            return "{} for 0 minutes".format(self.currentSummary)
        delta = (self.getTimeToChange() - self.__datehandler.currentTime()).seconds / 60
        return "{} for {} minutes".format(
            self.currentSummary,
            delta
        )

    def getTimeToChange(self):
        mins_to_change = self.__datehandler.getTimeDelta(minutes=self.minutesUntilChange)
        return self.__instantiation_time + mins_to_change

    def getTimeToTimeout(self):
        secs_to_change = self.__datehandler.getTimeDelta(seconds=self.checkTimeout)
        return self.__instantiation_time + secs_to_change


class DarkSky(object):

    def __init__(
        self,
        api_key,
        api_version="v1",
        http_interface = None,
        json_loads = None,
    ):
        self.__api_key = api_key
        self.__api_version = api_version
        self.__http = http_interface or HTTP()
        self.__json_loads = json_loads or json.loads
    
    def getWeather(
                self,
                latitude,
                longitude,
                forecast_type="forecast"
    ):
        response_code, response_body = self.__http.open(
            url = "https://api.darkskyapp.com/{}/{}/{}/{},{}".format(
                self.__api_version,
                forecast_type,
                self.__api_key,
                latitude,
                longitude
            )
        )
        return DarkSkyResponse(
            response_body=self.__json_loads(response_body),
            forecast_type=forecast_type
        )
