import pytest

pytestmark = [
    pytest.mark.requires_salt_modules("redis.example_function"),
]


@pytest.fixture
def redis(modules):
    return modules.redis


def test_replace_this_this_with_something_meaningful(redis):
    echo_str = "Echoed!"
    res = redis.example_function(echo_str)
    assert res == echo_str
