import time


def timed(func):
    def _func(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{round(end - start, 2)}s ({func.__name__})')
        return result
    return _func
