import asyncio
from typing import Any, Awaitable, Callable

__all__ = ["asyncio_entrypoint"]

def asyncio_entrypoint(func: Callable[..., Awaitable[...]]) -> Callable[..., Any]:
    """
    Function decorator to run an asynchronous main function by wrapping it
    with asyncio.run and awaiting.

    Must not be used if asyncio is already running.
    """
    def inner(*args, **kwargs): asyncio.run(func(*args, **kwargs))
    return inner
