from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def constant(val: T) -> Callable[..., T]:
    """Return a function that always yields ``val``."""

    def fun(*_):
        return val

    fun.__name__ = f"constant_{val}"

    return fun


def identity(val: T) -> T:
    """Return the input value unchanged."""

    return val
