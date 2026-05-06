from unittest.mock import MagicMock, patch

import pytest

from saltext.redis.returners import redis_return


@pytest.fixture
def configure_loader_modules():
    return {
        redis_return: {
            "__opts__": {
                "redis.host": "the mostest",
                "redis.port": 42,
                "redis.unix_socket_path": "the road less traveled",
                "redis.db": "13",
                "redis.password": "shibboleth",
                "redis.startup_nodes": {"lymph": "OK"},
                "redis.skip_full_coverage_check": True,
            }
        }
    }


@pytest.fixture(autouse=True)
def clean_REDIS_POOL():  # pylint: disable=invalid-name
    # Any unit test will want this value reset to None,
    # otherwise the values will remain set from other tests
    redis_return.REDIS_POOL = None


@pytest.fixture
def mock_strict_redis():
    with patch.object(redis_return, "redis", create=True):
        with patch("saltext.redis.returners.redis_return.redis.StrictRedis") as fake_strict_redis:
            yield fake_strict_redis


@pytest.fixture
def proxy_platform():
    with patch("salt.utils.platform.is_proxy", autospec=True, return_value=True):
        yield


@pytest.fixture
def non_proxy_platform():
    with patch("salt.utils.platform.is_proxy", autospec=True, return_value=False):
        yield


@pytest.fixture
def mock_returner_options():
    options = {
        "host": "some other hosty mchostface",
        "port": 99,
        "unix_socket_path": "something socket",
        "db": "cooper",
        "password": "super secret!",
    }
    with patch("salt.returners.get_returner_options", autospec=True, return_value=options):
        yield options


def test_when_platform_is_proxy_redis_should_use_opts_values(proxy_platform, mock_strict_redis):
    redis_return._get_serv()

    mock_strict_redis.assert_called_once_with(
        host="the mostest",
        port=42,
        unix_socket_path="the road less traveled",
        password="shibboleth",
        db="13",
        decode_responses=True,
    )


def test_when_platform_is_proxy_and_no_opts_are_set_fallback_values_should_be_used(
    proxy_platform, mock_strict_redis
):
    with patch.dict(redis_return.__opts__, {}, clear=True):
        redis_return._get_serv()

    mock_strict_redis.assert_called_once_with(
        host="salt",
        port=6379,
        unix_socket_path=None,
        db="0",
        password=None,
        decode_responses=True,
    )


def test_when_platform_is_not_proxy_it_should_use_returner_opts(
    non_proxy_platform, mock_strict_redis, mock_returner_options
):
    redis_return._get_serv()

    mock_strict_redis.assert_called_once_with(
        host="some other hosty mchostface",
        port=99,
        unix_socket_path="something socket",
        db="cooper",
        password="super secret!",
        decode_responses=True,
    )


# ---------------------------------------------------------------------------
# get_jids / clean_old_jobs: SCAN replaces blocking KEYS
# ---------------------------------------------------------------------------


def _serv_with_scan(scan_data, mget_data=None):
    """
    Build a ``serv`` mock whose ``scan_iter(match=...)`` returns the
    keys for a given pattern, plus a ``keys(...)`` that raises -- so
    the test fails loudly if the production code falls back to ``KEYS``.
    """
    serv = MagicMock(name="redis_serv")

    def fake_scan_iter(match=None, **kwargs):
        return iter(scan_data.get(match, []))

    def fake_keys(*args, **kwargs):
        raise AssertionError(
            "production code called serv.keys(...); it must use "
            "scan_iter() instead to avoid blocking the Redis server"
        )

    serv.scan_iter.side_effect = fake_scan_iter
    serv.keys.side_effect = fake_keys
    if mget_data is not None:
        serv.mget.return_value = mget_data
    return serv


def test_get_jids_uses_scan_iter_not_keys():
    """
    Headline regression: ``get_jids`` must walk the keyspace with
    ``SCAN``, not the blocking ``KEYS load:*``.
    """
    serv = _serv_with_scan(
        scan_data={"load:*": ["load:20240101", "load:20240102"]},
        mget_data=[None, None],  # contents don't matter for this test
    )
    with patch.object(redis_return, "_get_serv", return_value=serv):
        redis_return.get_jids()

    matches = [call.kwargs.get("match") for call in serv.scan_iter.call_args_list]
    assert "load:*" in matches


def test_get_jids_handles_no_jobs():
    """
    With no ``load:*`` keys in Redis, ``get_jids`` must return an empty
    dict (and must not call ``mget`` with an empty list, which some
    Redis clients reject). Pins the behaviour after the SCAN switch.
    """
    serv = _serv_with_scan(scan_data={"load:*": []})
    with patch.object(redis_return, "_get_serv", return_value=serv):
        result = redis_return.get_jids()

    assert result == {}
    serv.mget.assert_not_called()


def test_clean_old_jobs_uses_scan_iter_not_keys():
    """
    Headline regression: ``clean_old_jobs`` must enumerate both
    ``ret:*`` and ``load:*`` via ``SCAN``. Both calls were blocking
    ``KEYS`` before the fix.
    """
    serv = _serv_with_scan(
        scan_data={
            "ret:*": ["ret:20240101", "ret:20240102"],
            "load:*": ["load:20240102"],
        }
    )
    with patch.object(redis_return, "_get_serv", return_value=serv):
        redis_return.clean_old_jobs()

    matches = [call.kwargs.get("match") for call in serv.scan_iter.call_args_list]
    assert "ret:*" in matches
    assert "load:*" in matches


def test_clean_old_jobs_removes_only_orphan_ret_keys():
    """
    End-to-end behaviour after the SCAN switch: ``ret:<jid>`` keys
    whose ``load:<jid>`` counterpart no longer exists must be deleted.
    Active jobs (``ret`` with a matching ``load``) must be left alone.
    """
    serv = _serv_with_scan(
        scan_data={
            "ret:*": ["ret:dead-jid", "ret:alive-jid"],
            "load:*": ["load:alive-jid"],
        }
    )
    with patch.object(redis_return, "_get_serv", return_value=serv):
        redis_return.clean_old_jobs()

    serv.delete.assert_called_once()
    deleted = set(serv.delete.call_args.args)
    assert deleted == {"ret:dead-jid"}


def test_clean_old_jobs_no_orphans_no_delete():
    """No orphan keys -> no delete call. Pins backward compatibility."""
    serv = _serv_with_scan(
        scan_data={
            "ret:*": ["ret:alive"],
            "load:*": ["load:alive"],
        }
    )
    with patch.object(redis_return, "_get_serv", return_value=serv):
        redis_return.clean_old_jobs()

    serv.delete.assert_not_called()
