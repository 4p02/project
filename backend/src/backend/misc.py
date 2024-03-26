"""Miscellaneous decorators and utility functions."""

import asyncio
from typing import Any, Awaitable, Callable, Union
import functools
from urllib.parse import urlparse
import socket
from ipaddress import ip_network

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


# All of the IPs used to
(_, _, PRIVATE_HOST_IPS) = socket.gethostbyname_ex(socket.gethostname())

# https://en.wikipedia.org/wiki/Reserved_IP_addresses
PRIVATE_NETWORKS = [
    ip_network("0.0.0.0/8"),
    ip_network("10.0.0.0/8"),
    ip_network("100.64.0.0/10"),
    ip_network("127.0.0.0/8"),
    ip_network("169.254.0.0/16"),
    ip_network("172.16.0.0/12"),
    ip_network("192.0.0.0/24"),
    ip_network("192.0.2.0/24"),
    ip_network("192.88.99.0/24"),
    ip_network("192.168.0.0/16"),
    ip_network("198.18.0.0/15"),
    ip_network("198.51.100.0/24"),
    ip_network("203.0.113.0/24"),
    ip_network("224.0.0.0/4"),
    ip_network("233.252.0.0/24"),
    ip_network("240.0.0.0/4"),
    ip_network("255.255.255.255/32"),
    *(ip_network(ip) for ip in PRIVATE_HOST_IPS)
]


def check_valid_url(url: str) -> bool:
    """
    Check if the given URL is valid.
    """
    parsed = urlparse(url)

    if parsed.scheme == "" or parsed.hostname is None:
        return False

    # don't allow protocols other than http (like ftp://)
    if parsed.scheme != "http" and parsed.scheme != "https":
        return False

    # if host is a hostname: resolve the hostname into it's canonical ip
    # if host is an ip: normalize the ip address
    try:
        (_, _, url_ips) = socket.gethostbyaddr_ex(parsed.hostname)
        hostname_ips = [ip_address(ip) for ip in url_ips]
    except socket.gaierror:
        return False

    # then check if the all the hostname ip addresses are outside a private or local subnet
    if not all(hostname_ip not in network for hostname_ip in hostname_ips for network in PRIVATE_NETWORKS):
        return False

    return url
