import time
from functools import wraps
import asyncio

def time_logger(func):
    """
    Decorator to log execution time of async functions.
    Usage:
        @async_time_logger
        async def my_func(...):
            ...
    """
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)  # await async function
            end = time.time()
            print(f"[{func.__name__}] Execution time: {end-start:.3f}s")
            return result
        return wrapper
    else:
        # If the function is sync, fallback to normal timing
        @wraps(func)
        def wrapper_sync(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"[{func.__name__}] Execution time: {end-start:.3f}s")
            return result
        return wrapper_sync
