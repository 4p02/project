"""Miscellaneous decorators and utility functions."""

import asyncio
from typing import Any, Awaitable, Callable, Union
import functools
from urllib.parse import urlparse

from backend import logger

def decorator_args(
    decorator: Callable[[Callable[..., Any], ...], Callable[..., Any]]
) -> Callable[..., Callable[..., Callable[..., Any]]]:
    """
    Decorator decorator that forwards arguments to the decorator, if provided.
    Also ensures that decorators wrap the decorated function.
    """

    @functools.wraps(decorator)
    def decorator_wrapper(*args, **kwargs):
        @functools.wraps(decorator)
        def inner_wrapper(func: Callable[..., Any]) -> Any:
            new_func = decorator(func, *args, **kwargs)
            new_func = functools.wraps(func)(new_func)
            return new_func

        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            func = args[0]
            new_func = decorator(func, *args[1:], **kwargs)
            new_func = functools.wraps(func)(new_func)
            return new_func
        else:
            return inner_wrapper
    return decorator_wrapper


@decorator_args
def asyncio_entrypoint(func: Callable[..., Awaitable[...]]) -> Callable[..., Any]:
    """
    Function decorator to run an asynchronous main function by wrapping it
    with asyncio.run and awaiting.

    Must not be used if asyncio is already running.
    """
    def inner(*args, **kwargs): asyncio.run(func(*args, **kwargs))
    return inner


@decorator_args
def handle_and_log_exceptions(
    func: Callable[..., Union[Awaitable[...], Any]],
    *, default: Union[None, Any] = None, reraise: Union[None, Any] = None
) -> Callable[..., Union[Awaitable[...], Any]]:

    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            logger.error("Internal exception raised:", exc_info=ex)
            if reraise is not None: raise reraise
            return default

    async def inner_async(*args, **kwargs):
        try:
            async for val in func(*args, **kwargs):
                yield val
        # if the inner generator returned, it's didn't crash, so return as well
        except StopAsyncIteration as ex:
            raise ex
        except Exception as ex:
            logger.error("Internal exception raised:", exc_info=ex)
            if reraise is not None: raise reraise
            raise StopAsyncIteration(default)

    return inner_async if asyncio.iscoroutinefunction(func) else inner


def bytes_to_str(data: bytes) -> str:
    """
    Convert bytes to string.
    """
    return data.decode("utf-8")

def str_to_bytes(data: str) -> bytes:
    """
    Convert string to bytes.
    """
    return data.encode("utf-8")

def check_valid_url(url: str):
    """
    Check if the given URL is valid.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        return False
    # check if url is localhost or an ip address which is not allowed for security things
    if urlparse(url).hostname in ["localhost", "127.0.0.1", "0.0.0.0"]:
        return False
    elif urlparse(url).hostname is None:
        return False
    
    print(url)
    return url