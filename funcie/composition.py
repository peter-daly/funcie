from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def _callable_name(func: Callable[..., Any]) -> str:
    name = getattr(func, "__name__", "")
    if isinstance(name, str) and name:
        return name
    return func.__class__.__name__


class composable:
    """Callable wrapper with composition operators.

    - ``a >> b`` pipes output of ``a`` into ``b``
    - ``a << b`` composes ``a`` after ``b``
    - ``a @ b`` runs both on the same input and returns a tuple
    """

    def __init__(self, func: Callable[..., Any]):
        self.func = _as_callable(func)
        self.__name__ = _callable_name(self.func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

    def __rshift__(self, other: Any) -> "composable":
        """Pipe: ``self`` then ``other``."""

        other_func = _as_callable(other)

        def _piped(*args: Any, **kwargs: Any) -> Any:
            return other_func(self.func(*args, **kwargs))

        _piped.__name__ = f"{self.__name__}_then_{_callable_name(other_func)}"
        return composable(_piped)

    def __rrshift__(self, other: Any) -> "composable":
        return composable(_as_callable(other)) >> self

    def __lshift__(self, other: Any) -> "composable":
        """Compose: ``self`` after ``other``."""

        other_func = _as_callable(other)

        def _composed(*args: Any, **kwargs: Any) -> Any:
            return self.func(other_func(*args, **kwargs))

        _composed.__name__ = f"{self.__name__}_after_{_callable_name(other_func)}"
        return composable(_composed)

    def __rlshift__(self, other: Any) -> "composable":
        return composable(_as_callable(other)) << self

    def __matmul__(self, other: Any) -> "composable":
        """Juxt: run ``self`` and ``other`` on the same arguments."""

        other_func = _as_callable(other)

        def _juxted(*args: Any, **kwargs: Any) -> tuple[Any, Any]:
            return self.func(*args, **kwargs), other_func(*args, **kwargs)

        _juxted.__name__ = f"{self.__name__}_juxt_{_callable_name(other_func)}"
        return composable(_juxted)

    def __rmatmul__(self, other: Any) -> "composable":
        return composable(_as_callable(other)) @ self

    def __repr__(self) -> str:
        return f"composable({self.__name__})"


def _as_callable(func: Any) -> Callable[..., Any]:
    if isinstance(func, composable):
        return func.func
    if callable(func):
        return func
    raise TypeError("expected a callable")


def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Compose callables from right to left into a single callable."""

    if not funcs:
        raise ValueError("compose requires at least one function")

    wrapped = composable(_as_callable(funcs[0]))
    for func in funcs[1:]:
        wrapped = wrapped << func
    return wrapped


def pipe(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Compose callables from left to right into a single callable."""

    if not funcs:
        raise ValueError("pipe requires at least one function")

    wrapped = composable(_as_callable(funcs[0]))
    for func in funcs[1:]:
        wrapped = wrapped >> func
    return wrapped


def juxt(*funcs: Callable[..., Any]) -> Callable[..., tuple[Any, ...]]:
    """Apply all callables to the same arguments and return a result tuple."""

    callable_funcs = tuple(_as_callable(func) for func in funcs)

    def _juxtaposed(*args: Any, **kwargs: Any) -> tuple[Any, ...]:
        return tuple(func(*args, **kwargs) for func in callable_funcs)

    _juxtaposed.__name__ = "juxt_" + "_".join(_callable_name(func) for func in callable_funcs)
    return _juxtaposed


def flip(func: Callable[..., T]) -> Callable[..., T]:
    """Return a wrapper that swaps the first two positional arguments."""

    callable_func = _as_callable(func)

    def _flipped(*args: Any, **kwargs: Any) -> T:
        if len(args) < 2:
            raise TypeError("flip requires at least two positional arguments")

        swapped = (args[1], args[0], *args[2:])
        return callable_func(*swapped, **kwargs)

    _flipped.__name__ = f"flip_{_callable_name(callable_func)}"
    return _flipped


def tap(side_effect: Callable[[T], Any]) -> Callable[[T], T]:
    """Run a side effect with a value and then return the original value."""

    effect = _as_callable(side_effect)

    def _tap(value: T) -> T:
        effect(value)
        return value

    _tap.__name__ = f"tap_{_callable_name(effect)}"
    return _tap


__all__ = ["composable", "compose", "pipe", "juxt", "flip", "tap"]
