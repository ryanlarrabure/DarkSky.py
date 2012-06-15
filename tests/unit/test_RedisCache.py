from darksky.abstract_io.redis import RedisCache
import mock
from nose.tools import assert_equals, assert_dict_equal, assert_raises

def test_RedisCache():
    mock_strictredis = mock.Mock()
    internal_table = {}

    def mock_set(key, value):
        internal_table[key] = value
    mock_strictredis.set.side_effect = mock_set

    def mock_get(key):
        if key == "doesn't_exist":
            return None
        return internal_table[key]
    mock_strictredis.get.side_effect = mock_get

    instance = RedisCache(strict_redis=mock_strictredis)
    
    instance.insert("something", 1)
    yield (
        assert_equals,
        ("something", 1),
        mock_strictredis.set.call_args[0]
    )

    instance.insert("else", 2, 3)
    yield (
        assert_equals,
        ("else", 2),
        mock_strictredis.set.call_args[0]
    )
    yield (
        assert_equals,
        ("else", 3),
        mock_strictredis.expire.call_args[0]
    )

    yield (
        assert_equals,
        1,
        instance.get("something")
    )

    redis_mock = mock.Mock()
    redis_mock.StrictRedis.return_value.get.side_effect = mock_get
    args = {
        "hostname": "something",
        "password": "something",
        "port": 123,
        "db": 1,
    }

    instance = RedisCache(
        redis=redis_mock,
        **args
    )

    yield (
        assert_dict_equal,
        args,
        redis_mock.StrictRedis.call_args[1]
    )

    yield (
        assert_raises,
        KeyError,
        instance.get,
        "doesn't_exist"
    )
