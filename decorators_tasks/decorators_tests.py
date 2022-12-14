from unittest.mock import Mock

import pytest

from decorators_tasks.task04 import summ, multiply, CACHE
from decorators_tasks.task05 import retry


@pytest.fixture(scope="function")
def clear_cache():
    CACHE.clear()


def test_cache_decorator(clear_cache):
    assert summ(1, 2) == 3
    assert summ(x=1, y=2) == 3
    assert multiply(3, 4) == 12
    assert summ(2, 3) == 5

    assert CACHE == {('multiply', (("x", 3), ("y", 4))): 12, ('summ', (("x", 1), ("y", 2))): 3,
                     ('summ', (("x", 2), ("y", 3))): 5}


def test_cache_decorator_with_default_args(clear_cache):
    assert summ(1) == 1
    assert summ(1, 0) == 1
    assert summ(0, 1) == 1

    assert CACHE == {('summ', (("x", 1), ("y", 0))): 1, ('summ', (("x", 0), ("y", 1))): 1}


def test_cache_decorator_with_keyword_args(clear_cache):
    assert summ(x=2, y=3) == 5
    assert summ(y=3, x=2) == 5
    assert summ(3, 2) == 5

    assert CACHE == {('summ', (("x", 2), ("y", 3))): 5, ('summ', (("x", 3), ("y", 2))): 5}


def test_retry_decorator():
    mock_raise_exception_func = Mock(side_effect=[KeyError, 1])
    parametrized_log_func = retry(4, 5, (KeyError, ZeroDivisionError))
    decorated_func = parametrized_log_func(mock_raise_exception_func)
    result = decorated_func(1)
    assert result == 1


@pytest.mark.parametrize("side_effect, returned_exception",
                         [((KeyError, KeyError, ZeroDivisionError), "ZeroDivisionError"),
                          ((Exception, KeyError), "Exception")])
def test_retry_decorator_with_exception(side_effect, returned_exception):
    mock_raise_exception_func = Mock(side_effect=side_effect)
    parametrized_log_func = retry(3, 5, (KeyError, ZeroDivisionError))
    decorated_func = parametrized_log_func(mock_raise_exception_func)
    with pytest.raises(Exception) as exception_info:
        decorated_func(1)
    assert exception_info.typename == returned_exception


@pytest.mark.parametrize("attempts, poll_time",
                         [(0, 5), (3, -2)])
def test_retry_decorator_with_incorrect_decorator_args(attempts, poll_time):
    mock_raise_exception_func = Mock(side_effect=1)
    parametrized_log_func = retry(attempts, poll_time, (KeyError, ZeroDivisionError))
    decorated_func = parametrized_log_func(mock_raise_exception_func)
    with pytest.raises(ValueError) as exception_info:
        decorated_func(1)
    assert str(exception_info.value) == f"Incorrect value for attempts: {attempts} or poll_time: {poll_time}"
