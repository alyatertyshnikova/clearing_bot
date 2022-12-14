"""
You need to implement a decorator function `cache` that should be applied to some pure function.
Its goal is to save in cache all the function execution results.
"""
import inspect
from typing import Callable, Any

CACHE = {}


def cache(f: Callable) -> Callable:
    def wrapped_func(*args, **kwargs) -> Any:
        cache_args = {
            k: v.default
            for k, v in inspect.signature(f).parameters.items()
            if v.default is not inspect.Parameter.empty
        }
        args_dict = dict(zip(f.__code__.co_varnames, args))
        cache_args.update(args_dict)
        cache_args.update(kwargs)
        cache_args = tuple(sorted(cache_args.items()))

        cache_id = (f.__name__, cache_args)

        if cache_id in CACHE:
            return CACHE[cache_id]

        result = f(*args, **kwargs)
        CACHE.update({cache_id: result})
        return result

    return wrapped_func


@cache
def summ(x: int, y: int = 0) -> int:
    return x + y


@cache
def multiply(x: int, y: int) -> int:
    return x * y

