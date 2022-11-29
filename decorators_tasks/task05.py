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
from time import sleep
from typing import Callable, Tuple, Type, Any


def retry(attempts: int, poll_time: int, exceptions: Tuple[Type[Exception], ...] = (Exception,)) -> Callable:
    def decorator(f: Callable) -> Callable:
        def wrapped_func(*args, **kwargs) -> Any:
            current_attempt = 0
            last_exception = Exception
            while current_attempt < attempts:
                try:
                    result = f(*args, **kwargs)
                    return result
                except exceptions as ex:
                    last_exception = ex
                    current_attempt += 1
                    sleep(poll_time)
            raise last_exception

        return wrapped_func

    return decorator


@retry(attempts=4, poll_time=5, exceptions=(KeyError, ZeroDivisionError))
def raise_exception_func(x: int) -> int:
    return x
