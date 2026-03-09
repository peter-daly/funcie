from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature
from typing import Any, TypeVar

T = TypeVar("T")


def curry_n(n: int, func: Callable[..., T]) -> Callable[..., Any]:
    """Curry ``func`` to arity ``n`` using positional arguments only."""

    if n <= 0:
        raise ValueError("curry_n requires n >= 1")

    def _next(collected: tuple[Any, ...]) -> Callable[..., Any]:
        @wraps(func)
        def _curried(*args: Any, **kwargs: Any) -> Any:
            if kwargs:
                raise TypeError("curried functions do not support keyword arguments")
            if not args:
                raise TypeError("curried functions require at least one positional argument")

            merged = (*collected, *args)
            if len(merged) >= n:
                return func(*merged)
            return _next(merged)

        return _curried

    return _next(())


def curry(func: Callable[..., T]) -> Callable[..., Any]:
    """Infer positional arity for ``func`` and return a curried wrapper."""

    sig = signature(func)

    required_positional = 0
    for param in sig.parameters.values():
        if param.kind is Parameter.VAR_POSITIONAL:
            raise ValueError("curry does not support functions with *args")
        if param.kind is Parameter.KEYWORD_ONLY and param.default is Parameter.empty:
            raise ValueError("curry does not support required keyword-only parameters")
        if param.kind in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
            if param.default is not Parameter.empty:
                raise ValueError("curry does not support positional parameters with defaults")
            required_positional += 1

    if required_positional == 0:
        raise ValueError("curry requires at least one required positional parameter")

    return curry_n(required_positional, func)


def curried(func: Callable[..., T] | None = None, *, n: int | None = None) -> Callable[..., Any]:
    """Decorator that curries a function using ``curry`` or ``curry_n``.

    Use as ``@curried`` to infer arity, or ``@curried(n=...)`` to set arity explicitly.
    """

    def _apply(target: Callable[..., T]) -> Callable[..., Any]:
        if n is None:
            return curry(target)
        return curry_n(n, target)

    if func is None:
        return _apply

    return _apply(func)


__all__ = ["curry", "curry_n", "curried"]
