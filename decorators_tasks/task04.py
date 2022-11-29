"""
You need to implement a decorator function `cache` that should be applied to some pure function.
Its goal is to save in cache all the function execution results.
"""
from typing import Callable, Any

CACHE = {}


def cache(f: Callable) -> Callable:
    def wrapped_func(*args, **kwargs) -> Any:
        if f.__name__ in CACHE.keys():
            return CACHE[f.__name__]
        result = f(*args, **kwargs)
        CACHE.update({f.__name__: result})
        return result

    return wrapped_func


@cache
def summ(x: int, y: int) -> int:
    return x + y


@cache
def multiply(x: int, y: int) -> int:
    return x * y

