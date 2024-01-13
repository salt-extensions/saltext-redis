import pytest
import saltext.redis.sdb.redis_mod as redis_sdb


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        redis_sdb: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in redis_sdb.__salt__
    assert redis_sdb.__salt__["this_does_not_exist.please_replace_it"]() is True
