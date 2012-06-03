import darksky.abstract_io.DateHandler as DateHandler
import mock
from nose.tools import assert_equals, assert_true

def test_toDatetime():
    mock_utcfromtimestamp = mock.Mock()
    mock_utcfromtimestamp.return_value = "Something"
    instance = DateHandler(
        utcfromtimestamp = mock_utcfromtimestamp,
        utcnow = mock.Mock(),
        timedelta = mock.Mock()
    )

    yield (
        assert_equals,
        "Something",
        instance.toDatetime(1234)
    )

    yield (
        assert_equals,
        1234,
        mock_utcfromtimestamp.call_args[0][0]
    )

def test_currentTime():
    mock_utcnow = mock.Mock() 
    mock_utcnow.return_value = "something"
    instance = DateHandler(
        utcfromtimestamp = mock.Mock(),
        utcnow = mock_utcnow,
        timedelta = mock.Mock()
    )

    yield (
        assert_equals,
        "something",
        instance.currentTime()
    )

def test_getTimeDelta():
    mock_timedelta = mock.Mock() 
    mock_timedelta.return_value = "something"
    instance = DateHandler(
        utcfromtimestamp = mock.Mock(),
        utcnow = mock.Mock(),
        timedelta = mock_timedelta
    )

    yield (
        assert_equals,
        "something",
        instance.getTimeDelta(1, 2, something=3)
    )
    
    yield (
        assert_equals,
        (1, 2),
        mock_timedelta.call_args[0]
    )

    yield (
        assert_equals,
        {"something":3},
        mock_timedelta.call_args[1]
    )
