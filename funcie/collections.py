from collections.abc import Callable, Iterable, Iterator
from functools import reduce
from itertools import chain, islice, tee
from typing import Any, TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

_MISSING = object()


def keep(pred: Callable[[T], bool], iterable: Iterable[T]) -> Iterator[T]:
    """Lazily keep values where ``pred`` returns ``True``."""

    return (item for item in iterable if pred(item))


def reject(pred: Callable[[T], bool], iterable: Iterable[T]) -> Iterator[T]:
    """Lazily keep values where ``pred`` returns ``False``."""

    return (item for item in iterable if not pred(item))


def flat_map(func: Callable[[T], Iterable[U]], iterable: Iterable[T]) -> Iterator[U]:
    """Lazily map and flatten one level of nested iterables."""

    return chain.from_iterable(func(item) for item in iterable)


def take(n: int, iterable: Iterable[T]) -> Iterator[T]:
    """Return a lazy iterator over the first ``n`` items."""

    if n < 0:
        raise ValueError("take requires n >= 0")
    return islice(iterable, n)


def drop(n: int, iterable: Iterable[T]) -> Iterator[T]:
    """Return a lazy iterator that skips the first ``n`` items."""

    if n < 0:
        raise ValueError("drop requires n >= 0")
    return islice(iterable, n, None)


def partition(pred: Callable[[T], bool], iterable: Iterable[T]) -> tuple[Iterator[T], Iterator[T]]:
    """Split values into lazy matching and non-matching iterators."""

    left, right = tee(iterable)
    return keep(pred, left), reject(pred, right)


def fold(func: Callable[[Any, Any], Any], iterable: Iterable[Any], initial: Any = _MISSING) -> Any:
    """Reduce ``iterable`` with ``func``, optionally starting from ``initial``."""

    if initial is _MISSING:
        return reduce(func, iterable)
    return reduce(func, iterable, initial)


__all__ = [
    "keep",
    "reject",
    "flat_map",
    "take",
    "drop",
    "partition",
    "fold",
]
