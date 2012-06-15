import json
from abstract_io import HTTP, DateHandler, MemoryCache

class DarkSkyException(Exception):
    pass

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
        """Give the current hour summary.

        Dynamic property.  Will always return the time to change relative to
        the time of accessing the property.
        
        """
        time_field = ""
        if self.__datehandler.currentTime() >= self.getTimeToChange():
            return "{} for 0 minutes".format(self.currentSummary)
        delta = (self.getTimeToChange()
                 - self.__datehandler.currentTime()
        ).seconds / 60
        return "{} for {} minutes".format(
            self.currentSummary,
            delta
        )

    def getTimeToChange(self):
        """Calculate the time to change.
        
        Returns the timedelta between now and the time to change.
        
        """
        mins_to_change = self.__datehandler.getTimeDelta(
            minutes=self.minutesUntilChange
        )
        return self.__instantiation_time + mins_to_change

    def getTimeToTimeout(self):
        """Calculate the time to timeout.

        Returns the timedelta between now and the time to timeout.

        """
        secs_to_change = self.__datehandler.getTimeDelta(
            seconds=self.checkTimeout
        )
        return self.__instantiation_time + secs_to_change


class DarkSky(object):
    darksky_url = "https://api.darkskyapp.com"

    def __init__(
        self,
        api_key,
        api_version="v1",
        http_interface = None,
        json_loads = None,
        DarkSkyResponseClass = None,
        datehandler = None,
        cache = None
    ):
        """
        api_key -- DarkSky api key
        api_version -- DarkSky api version (default: 'v1')
        """
        self.__api_key = api_key
        self.__api_version = api_version
        self.__http = http_interface or HTTP()
        self.__json_loads = json_loads or json.loads
        self.__DarkSkyResponse = DarkSkyResponseClass or DarkSkyResponse
        self.__datehandler = datehandler or DateHandler()
        self.__cache = cache or MemoryCache(timeout=3600)

    def __checkResponse(self, response_code, response_body):
        if response_code == 403:
            raise DarkSkyException("Invalid ApiKey presented")
        elif response_code != 200:
            raise DarkSkyException(
                "Expected '200' response; got '{}': {}".format(
                    response_code,
                    response_body
                )
            )
    
    def getWeather(
                self,
                latitude,
                longitude,
                forecast_type="forecast"
    ):
        """Get current weather for a location.
        
        Returns a DarkSkyResponse object.

        latitude -- latitude
        longitude -- longitude 
        forecast_type -- 'forecast' or 'brief' (default: forecast)
        
        """
        key = "{},{},{}".format(latitude,longitude,forecast_type)
        try:
            return self.__cache.get(key)
        except KeyError:
            response_code, response_body = self.__http.open(
                url = "{}/{}/{}/{}/{},{}".format(
                    self.darksky_url,
                    self.__api_version,
                    forecast_type,
                    self.__api_key,
                    latitude,
                    longitude
                )
            )
            self.__checkResponse(response_code, response_body)
            resp = self.__DarkSkyResponse(
                response_body=self.__json_loads(response_body),
                forecast_type=forecast_type
            )
            self.__cache.insert(key, resp, resp.checkTimeout)
            return resp

    def getInteresting(self):
        """Get interesting weather.

        Returns a list of storms.

        """
        url = "{}/{}/interesting/{}".format(
            self.darksky_url,
            self.__api_version,
            self.__api_key
        )
        try:
            return self.__cache.get(url)
        except KeyError:
            response_code, response_body = self.__http.open(url=url)
            self.__checkResponse(response_code, response_body)
            parsed_body = self.__json_loads(response_body)
            self.__cache.insert(url, parsed_body["storms"], 600)
            return parsed_body["storms"]
    
    def getWeathers(
        self,
        points
    ):
        """Get weather for multiple points.
            
        Points should be an iterable object of dicts.  The required dict fields
        are 'latitude' and 'longitude', both longs.  'time' is an optional
        argument, in DateTime format.
        
        points -- iterable object of coordinates and optional times

        """
        point_params = ""
        for point in points:
            out = "{},{}".format(point["latitude"], point["longitude"])
            if "time" in point:
                converted_time = self.__datehandler.timeTupleToUnix(
                    point["time"].utctimetuple()
                )
                out = "{},{}".format(out, converted_time)
            point_params = "{}{};".format(point_params, out)
        point_params = point_params.rstrip(";")
        url = "{}/{}/precipitation/{}/{}".format(
            self.darksky_url,
            self.__api_version,
            self.__api_key,
            point_params
        )
        try:
            return self.__cache.get(url)
        except KeyError:
            response_code, response_body = self.__http.open(url=url)
            self.__checkResponse(response_code, response_body)
            parsed_body = self.__json_loads(response_body)
            self.__cache.insert(url, parsed_body["precipitation"], 600)
            return parsed_body["precipitation"]
