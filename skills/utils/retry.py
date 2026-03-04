"""Retry helpers for Snowdrop skills."""
from __future__ import annotations

import random
import time
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")


def retry(
    attempts: int = 3,
    backoff_seconds: float = 0.5,
    jitter: float = 0.1,
    retriable_exceptions: Iterable[type[BaseException]] | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry decorator with exponential backoff and jitter.

    Args:
        attempts: Maximum number of attempts including the first call.
        backoff_seconds: Initial backoff delay before retrying.
        jitter: Random jitter added to each delay to avoid thundering herds.
        retriable_exceptions: Iterable of exception classes that should trigger retries.

    Returns:
        Decorated function that retries the call according to the provided policy.
    """

    exceptions: tuple[type[BaseException], ...] = (
        tuple(retriable_exceptions) if retriable_exceptions else (Exception,)
    )

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exc: BaseException | None = None
            delay = backoff_seconds
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt == attempts:
                        raise
                    sleep_for = delay + random.random() * jitter
                    time.sleep(max(sleep_for, 0))
                    delay *= 2
            raise last_exc if last_exc else RuntimeError("retry wrapper failed without exception")

        return wrapper

    return decorator


def retry_call(
    func: Callable[..., T],
    *args: Any,
    attempts: int = 3,
    backoff_seconds: float = 0.5,
    jitter: float = 0.1,
    retriable_exceptions: Iterable[type[BaseException]] | None = None,
    **kwargs: Any,
) -> T:
    """Retry an arbitrary callable without using decorator syntax.

    Args:
        func: Callable to execute with retries.
        *args: Positional arguments for the callable.
        attempts: Maximum attempts including the first try.
        backoff_seconds: Initial backoff delay before retrying.
        jitter: Random jitter added to each delay.
        retriable_exceptions: Iterable of exception types that should be retried.
        **kwargs: Keyword arguments for the callable.

    Returns:
        The callable's return value after a successful attempt.

    Raises:
        The last encountered exception once attempts are exhausted.
    """

    retry_wrapper = retry(
        attempts=attempts,
        backoff_seconds=backoff_seconds,
        jitter=jitter,
        retriable_exceptions=retriable_exceptions,
    )
    return retry_wrapper(func)(*args, **kwargs)
