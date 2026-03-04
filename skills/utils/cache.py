import functools
import time
from typing import Callable, Any

def memory_cache(ttl_seconds: int = 3600) -> Callable:
    """Simple in-memory cache decorator with TTL.

    Args:
        ttl_seconds: Time to live for cached items in seconds. Defaults to 1 hour.
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a hashable key from args and kwargs
            try:
                # Handle unhashable kwargs by converting lists/dicts to tuples/frozensets if necessary,
                # but for simplicity, we'll stringify kwargs if they are not hashable.
                # A robust approach for simple primitive kwargs:
                frozen_kwargs = frozenset((k, str(v) if isinstance(v, (list, dict)) else v) for k, v in kwargs.items())
                key = (args, frozen_kwargs)
            except TypeError:
                # Fallback if arguments are still unhashable
                key = str(args) + str(kwargs)

            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl_seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator
