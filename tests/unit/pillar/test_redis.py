import pytest
import saltext.redis.pillar.redis_mod as redis_pillar


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        redis_pillar: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in redis_pillar.__salt__
    assert redis_pillar.__salt__["this_does_not_exist.please_replace_it"]() is True
