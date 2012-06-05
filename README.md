# DarkSky.py

DarkSky.py is a Python interface to the DarkSky REST api.

## Requirements

- Python 2.7

## Installation

From the root of the repo:

    easy_install ./

That will pull in all the dependencies.


## Usage

### Using the DarkSky interface

Instantiate the DarkSky interface:

```python
import darksky

ds_interface = darksky.DarkSky("api_key_goes_here")
```

The following methods are implemented on the interface object:

- getWeather; for getting the weather on a particular location (returns a DarkSkyResponse object)

```python
current_weather = ds_interface.getWeather(
    latitude=1234.00,
    longitude=1235.11
)
```

- getInteresting; get a list of interesting storms
- getWeather; get weather for multiple points. With optional time elements.

```python
import datetime

conditions = ds_interface.getWeathers(
    points=[
        {
            "latitude":1234.0,
            "longitude":1234.11,
            "time":datetime.datetime(
                year=2012,
                month=6,
                day=4
            )
        },
        {
            "latitude":1235.0,
            "longitude":1235.11,
            "time":datetime.datetime(
                year=2012,
                month=6,
                day=3
            )
        },
    ]
)
```

### Using the DarkSkyResponse object

The DarkSkyResponse object has all the response properties set as object properties:

    >>> ds_response.currentTemp
    75
    >>> ds_response.currentSummary
    'light rain'
    >>> ds_response.hourSummary
    'light rain for 13 minutes'
    >>> ds_response.isPrecipitating
    True
    >>> cw.dayPrecipitation[0]
    {'type': 'rain', 'temp': 74, 'probability': 0.5586104718059857, 'time': datetime.datetime(2012, 5, 28, 14, 0)}

Note that dates are native Python date objects.  This also allows the special methods:

- getTimeToChange; return the time the change is predicted to occur
- getTimeToTimeout; return the time to the timeout

The hourSummary property is dynamic.  It will always be represented as the time from now until the event is to take place.  If you attempt to access it after the event has taken place, it will read "event for 0 minutes".

For example:

    >>> cw.hourSummary
    'light rain for 13 minutes'

Two minutes later:

    >>> cw.hourSummary
    'light rain for 11 minutes'

## Running the tests

1. Install the requirements (not included in setup.py)

    pip install -r requirements.txt

2. From the src directory, execute the tests

    nosetests ../tests/*

## License

Copyright (c) 2012, Ryan Larrabure
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of the Ryan Larrabure nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

