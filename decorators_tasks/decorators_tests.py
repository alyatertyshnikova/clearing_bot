from unittest.mock import Mock

import pytest

from decorators_tasks.task04 import summ, multiply, CACHE
from decorators_tasks.task05 import retry


def test_cache_decorator():
    assert summ(1, 2) == 3
    assert multiply(3, 4) == 12
    assert summ(2, 3) == 3
    assert CACHE == {'multiply': 12, 'summ': 3}


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
