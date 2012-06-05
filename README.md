# DarkSky.py

DarkSky.py is a Python interface to the DarkSky REST api.

## Requirements

Python 2.7.

## Installation

From the root of the repo:

    easy_install ./

That will pull in all the dependencies.


## Usage

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
            latitude=1234.0,
            longitude=1234.11,
            time=datetime.datetime(
                year=2012,
                month=6,
                day=4
            )
        },
        {
            latitude=1235.0,
            longitude=1235.11,
            time=datetime.datetime(
                year=2012,
                month=6,
                day=3
            )
        },
    ]
)
```

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

