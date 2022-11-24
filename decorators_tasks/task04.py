"""
You need to implement a decorator function `cache` that should be applied to some pure function.
Its goal is to save in cache all the function execution results.
"""
CACHE = []


def cache(f):
    def wrapped_func(x, y):
        result = f(x, y)
        CACHE.append(result)

    return wrapped_func


@cache
def summ(x, y):
    return x + y


@cache
def multiply(x, y):
    return x * y


# summ(1, 4)
# summ(1, 2)
# multiply(2, 3)
# print(CACHE)
