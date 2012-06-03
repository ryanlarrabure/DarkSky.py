import darksky.abstract_io.HTTP as HTTP
import mock
from nose.tools import assert_equals

def test_open():
    mock_get = mock.Mock()
    mock_get.return_value.status_code = 200 
    mock_get.return_value.text = "something"

    instance = HTTP(get=mock_get)
    
    response_code, data = instance.open("http://www.google.com")
    yield (
        assert_equals,
        200,
        response_code
    )

    yield (
        assert_equals,
        "something",
        data
    )

    yield (
        assert_equals,
        "http://www.google.com",
        mock_get.call_args[0][0]
    )
