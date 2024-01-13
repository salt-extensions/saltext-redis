import pytest
import salt.modules.test as testmod
import saltext.redis.modules.redis_mod as redis_module
import saltext.redis.states.redis_mod as redis_state


@pytest.fixture
def configure_loader_modules():
    return {
        redis_module: {
            "__salt__": {
                "test.echo": testmod.echo,
            },
        },
        redis_state: {
            "__salt__": {
                "redis.example_function": redis_module.example_function,
            },
        },
    }


def test_replace_this_this_with_something_meaningful():
    echo_str = "Echoed!"
    expected = {
        "name": echo_str,
        "changes": {},
        "result": True,
        "comment": f"The 'redis.example_function' returned: '{echo_str}'",
    }
    assert redis_state.exampled(echo_str) == expected
