"""
:codeauthor: Jayesh Kariya <jayeshk@saltstack.com>

Test cases for salt.modules.redismod
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from saltext.redis.modules import redismod


class Mockredis:
    """
    Mock redis class
    """

    class ConnectionError(Exception):
        """
        Mock ConnectionError class
        """


class MockConnect:
    """
    Mock Connect class
    """

    counter = 0

    def __init__(self):
        self.name = None
        self.pattern = None
        self.value = None
        self.key = None
        self.seconds = None
        self.timestamp = None
        self.field = None
        self.start = None
        self.stop = None
        self.master_host = None
        self.master_port = None

    @staticmethod
    def bgrewriteaof():
        """
        Mock bgrewriteaof method
        """
        return "A"

    @staticmethod
    def bgsave():
        """
        Mock bgsave method
        """
        return "A"

    def config_get(self, pattern):
        """
        Mock config_get method
        """
        self.pattern = pattern
        return "A"

    def config_set(self, name, value):
        """
        Mock config_set method
        """
        self.name = name
        self.value = value
        return "A"

    @staticmethod
    def dbsize():
        """
        Mock dbsize method
        """
        return "A"

    @staticmethod
    def delete():
        """
        Mock delete method
        """
        return "A"

    def exists(self, key):
        """
        Mock exists method
        """
        self.key = key
        return "A"

    def expire(self, key, seconds):
        """
        Mock expire method
        """
        self.key = key
        self.seconds = seconds
        return "A"

    def expireat(self, key, timestamp):
        """
        Mock expireat method
        """
        self.key = key
        self.timestamp = timestamp
        return "A"

    @staticmethod
    def flushall():
        """
        Mock flushall method
        """
        return "A"

    @staticmethod
    def flushdb():
        """
        Mock flushdb method
        """
        return "A"

    def get(self, key):
        """
        Mock get method
        """
        self.key = key
        return "A"

    def hget(self, key, field):
        """
        Mock hget method
        """
        self.key = key
        self.field = field
        return "A"

    def hgetall(self, key):
        """
        Mock hgetall method
        """
        self.key = key
        return "A"

    @staticmethod
    def info():
        """
        Mock info method
        """
        return "A"

    def keys(self, pattern):
        """
        Mock keys method
        """
        self.pattern = pattern
        return "A"

    def type(self, key):
        """
        Mock type method
        """
        self.key = key
        return "A"

    @staticmethod
    def lastsave():
        """
        Mock lastsave method
        """
        return datetime.now()

    def llen(self, key):
        """
        Mock llen method
        """
        self.key = key
        return "A"

    def lrange(self, key, start, stop):
        """
        Mock lrange method
        """
        self.key = key
        self.start = start
        self.stop = stop
        return "A"

    @staticmethod
    def ping():
        """
        Mock ping method
        """
        MockConnect.counter = MockConnect.counter + 1
        if MockConnect.counter == 1:
            return "A"
        elif MockConnect.counter in (2, 3, 5):
            raise Mockredis.ConnectionError("foo")

    @staticmethod
    def save():
        """
        Mock save method
        """
        return "A"

    def set(self, key, value):
        """
        Mock set method
        """
        self.key = key
        self.value = value
        return "A"

    @staticmethod
    def shutdown():
        """
        Mock shutdown method
        """
        return "A"

    def slaveof(self, master_host, master_port):
        """
        Mock slaveof method
        """
        self.master_host = master_host
        self.master_port = master_port
        return "A"

    def smembers(self, key):
        """
        Mock smembers method
        """
        self.key = key
        return "A"

    @staticmethod
    def time():
        """
        Mock time method
        """
        return "A"

    def zcard(self, key):
        """
        Mock zcard method
        """
        self.key = key
        return "A"

    def zrange(self, key, start, stop):
        """
        Mock zrange method
        """
        self.key = key
        self.start = start
        self.stop = stop
        return "A"


@pytest.fixture
def configure_loader_modules():
    return {
        redismod: {
            "redis": Mockredis,
            "_connect": MagicMock(return_value=MockConnect()),
        }
    }


def test_bgrewriteaof():
    """
    Test to asynchronously rewrite the append-only file
    """
    assert redismod.bgrewriteaof() == "A"


def test_bgsave():
    """
    Test to asynchronously save the dataset to disk
    """
    assert redismod.bgsave() == "A"


def test_config_get():
    """
    Test to get redis server configuration values
    """
    assert redismod.config_get("*") == "A"


def test_config_set():
    """
    Test to set redis server configuration values
    """
    assert redismod.config_set("name", "value") == "A"


def test_dbsize():
    """
    Test to return the number of keys in the selected database
    """
    assert redismod.dbsize() == "A"


def test_delete():
    """
    Test to deletes the keys from redis, returns number of keys deleted
    """
    assert redismod.delete() == "A"


def test_exists():
    """
    Test to return true if the key exists in redis
    """
    assert redismod.exists("key") == "A"


def test_expire():
    """
    Test to set a keys time to live in seconds
    """
    assert redismod.expire("key", "seconds") == "A"


def test_expireat():
    """
    Test to set a keys expire at given UNIX time
    """
    assert redismod.expireat("key", "timestamp") == "A"


def test_flushall():
    """
    Test to remove all keys from all databases
    """
    assert redismod.flushall() == "A"


def test_flushdb():
    """
    Test to remove all keys from the selected database
    """
    assert redismod.flushdb() == "A"


def test_get_key():
    """
    Test to get redis key value
    """
    assert redismod.get_key("key") == "A"


def test_hget():
    """
    Test to get specific field value from a redis hash, returns dict
    """
    assert redismod.hget("key", "field") == "A"


def test_hgetall():
    """
    Test to get all fields and values from a redis hash, returns dict
    """
    assert redismod.hgetall("key") == "A"


def test_info():
    """
    Test to get information and statistics about the server
    """
    assert redismod.info() == "A"


def test_keys():
    """
    Test to get redis keys, supports glob style patterns
    """
    assert redismod.keys("pattern") == "A"


def test_key_type():
    """
    Test to get redis key type
    """
    assert redismod.key_type("key") == "A"


def test_lastsave():
    """
    Test to get the UNIX time in seconds of the last successful
    save to disk
    """
    assert redismod.lastsave()


def test_llen():
    """
    Test to get the length of a list in Redis
    """
    assert redismod.llen("key") == "A"


def test_lrange():
    """
    Test to get a range of values from a list in Redis
    """
    assert redismod.lrange("key", "start", "stop") == "A"


def test_ping():
    """
    Test to ping the server, returns False on connection errors
    """
    assert redismod.ping() == "A"

    assert not redismod.ping()


def test_save():
    """
    Test to synchronously save the dataset to disk
    """
    assert redismod.save() == "A"


def test_set_key():
    """
    Test to set redis key value
    """
    assert redismod.set_key("key", "value") == "A"


def test_shutdown():
    """
    Test to synchronously save the dataset to disk and then
    shut down the server
    """
    assert not redismod.shutdown()

    assert redismod.shutdown()

    assert not redismod.shutdown()


def test_slaveof():
    """
    Test to make the server a slave of another instance, or
    promote it as master
    """
    assert redismod.slaveof("master_host", "master_port") == "A"


def test_smembers():
    """
    Test to get members in a Redis set
    """
    assert redismod.smembers("key") == ["A"]


def test_time():
    """
    Test to return the current server UNIX time in seconds
    """
    assert redismod.time() == "A"


def test_zcard():
    """
    Test to get the length of a sorted set in Redis
    """
    assert redismod.zcard("key") == "A"


def test_zrange():
    """
    Test to get a range of values from a sorted set in Redis by index
    """
    assert redismod.zrange("key", "start", "stop") == "A"
