import pytest
import saltext.redis.engines.redis_mod as redis_engine


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        redis_engine: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in redis_engine.__salt__
    assert redis_engine.__salt__["this_does_not_exist.please_replace_it"]() is True
