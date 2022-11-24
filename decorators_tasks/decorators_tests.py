import pytest

from decorators_tasks.task04 import summ, multiply, CACHE
from decorators_tasks.task05 import raise_exception_func


def test_cache_decorator():
    summ(1, 2)
    summ(2, 3)
    multiply(3, 4)
    assert CACHE == [3, 5, 12]


@pytest.mark.parametrize("input_value, expected_value",
                         [(1, -1), (2, 3), (3, 3)])
def test_retry_decorator(input_value, expected_value):
    result = raise_exception_func(input_value)
    assert result == expected_value
