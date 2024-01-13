import pytest

pytestmark = [
    pytest.mark.requires_salt_states("redis.exampled"),
]


@pytest.fixture
def redis(states):
    return states.redis


def test_replace_this_this_with_something_meaningful(redis):
    echo_str = "Echoed!"
    ret = redis.exampled(echo_str)
    assert ret.result
    assert not ret.changes
    assert echo_str in ret.comment
