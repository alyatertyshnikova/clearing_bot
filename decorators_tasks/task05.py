"""
During programming, we often need some retry mechanism. Usually such solution is made using
decorator pattern - we decorate the function that should be retried. The decorator has several parameters for
defining a number of attempts and the time period between attempts. Sometimes we can provide a list of exceptions
that should be retried.
Sample signature:
>>> from typing import Tuple, Callable
>>> def retry(attempts: int = 3, poll_time: int = 1, exceptions: Tuple[Exception, ...] = (Exception, )) -> Callable:
...     ...
"""
from time import time
from typing import Callable, Collection


def retry(attempts: int, exceptions: Collection, poll_time: int) -> Callable:

    def decorator(f: Callable) -> Callable:
        def wrapped_func(x: int):
            last_attempt_time = 0
            current_attempt = 0
            while current_attempt < attempts:
                if time()-last_attempt_time > poll_time:
                    try:
                        result = f(x)
                        return result
                    except exceptions:
                        x += 1
                        current_attempt += 1
                        last_attempt_time = time()
            return -1

        return wrapped_func

    return decorator


@retry(attempts=2, exceptions=(KeyError, ZeroDivisionError), poll_time=5)
def raise_exception_func(x: int):
    if x == 1:
        raise KeyError
    if x == 2:
        raise ZeroDivisionError
    return x


# print(raise_exception_func(3))