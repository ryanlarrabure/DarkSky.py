import mock
from nose.tools import assert_equals, assert_raises
from darksky import DarkSky
from darksky import DarkSkyException
import json

def test_getWeather_success():
    mock_http = mock.Mock()
    mock_dsresponse = mock.Mock()
    mock_dsresponse.return_value = "something"
    instance = DarkSky(
        api_key="abc",
        http_interface=mock_http,
        DarkSkyResponseClass=mock_dsresponse
    )
    mock_http.open.return_value = (
        200,
        json.dumps(
            {"data": True}
        )
    )
    ret_val = instance.getWeather(latitude=123, longitude=1234, forecast_type="brief")
    
    yield (
        assert_equals,
        "something",
        ret_val
    )

    yield (
        assert_equals,
        "https://api.darkskyapp.com/v1/brief/abc/123,1234",
        mock_http.open.call_args[1]["url"]
    )

    yield (
        assert_equals,
        {"data": True},
        mock_dsresponse.call_args[1]["response_body"]
    )

    yield (
        assert_equals,
        "brief",
        mock_dsresponse.call_args[1]["forecast_type"]
    )

def test_getWeather_failure():
    mock_http = mock.Mock()
    instance = DarkSky(
        api_key="abc",
        http_interface=mock_http
    )
    mock_http.open.return_value = (
        403,
        json.dumps(
            {
                "code": 403,
                "error": "Forbidden"
            }
        )
    )
    yield (
        assert_raises,
        DarkSkyException,
        instance.getWeather,
        123,
        1234,
        "brief"
    )
