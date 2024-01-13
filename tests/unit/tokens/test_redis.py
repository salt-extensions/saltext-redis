import pytest
import saltext.redis.tokens.redis_mod as redis_token


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        redis_token: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in redis_token.__salt__
    assert redis_token.__salt__["this_does_not_exist.please_replace_it"]() is True
