from collections.abc import Callable
from typing import Any

from .core import constant

Predicate = Callable[..., bool]


def _callable_name(func: Predicate) -> str:
    name = getattr(func, "__name__", "")
    if isinstance(name, str) and name:
        return name
    return func.__class__.__name__


class predicate:
    """
    A class representing a predicate function.

    Predicates are callable objects that take arguments and return a boolean value.
    They can be combined using logical operators like `and`, `or`, and `not`.

    Attributes:
        func (Callable[..., bool]): The underlying function representing the predicate.

    Methods:
        __init__(self, func: Callable[..., bool]): Initializes a new instance of the predicate class.
        __call__(self, *args, **kwargs): Calls the underlying function with the given arguments.
        __and__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `and` operator.
        __rand__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `and` operator (reversed).
        __or__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `or` operator.
        __ror__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `or` operator (reversed).
        __xor__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `xor` (exclusive or) operator.
        __rxor__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `xor` (exclusive or) operator (reversed).
        __invert__(self): Negates the predicate using the `not` operator.
        __repr__(self) -> str: Returns a string representation of the predicate.
    """

    def __init__(self, func: Predicate):
        self.func = func
        self.__name__ = _callable_name(func)

    def __call__(self, *args: Any, **kwargs: Any) -> bool:
        return self.func(*args, **kwargs)

    def __and__(self, other: Predicate) -> "predicate":
        def _and(*args: Any, **kwargs: Any) -> bool:
            return self.func(*args, **kwargs) and other(*args, **kwargs)

        _and.__name__ = f"{self.__name__}_and_{_callable_name(other)}"

        return predicate(_and)

    def __rand__(self, other: Predicate) -> "predicate":
        def _and(*args: Any, **kwargs: Any) -> bool:
            return other(*args, **kwargs) and self.func(*args, **kwargs)

        _and.__name__ = f"{_callable_name(other)}_and_{self.__name__}"

        return predicate(_and)

    def __or__(self, other: Predicate) -> "predicate":
        def _or(*args: Any, **kwargs: Any) -> bool:
            return self.func(*args, **kwargs) or other(*args, **kwargs)

        _or.__name__ = f"{self.__name__}_or_{_callable_name(other)}"
        return predicate(_or)

    def __ror__(self, other: Predicate) -> "predicate":
        def _or(*args: Any, **kwargs: Any) -> bool:
            return other(*args, **kwargs) or self.func(*args, **kwargs)

        _or.__name__ = f"{_callable_name(other)}_or_{self.__name__}"
        return predicate(_or)

    def __xor__(self, other: Predicate) -> "predicate":
        def _xor(*args: Any, **kwargs: Any) -> bool:
            return self.func(*args, **kwargs) ^ other(*args, **kwargs)

        _xor.__name__ = f"{self.__name__}_xor_{_callable_name(other)}"
        return predicate(_xor)

    def __rxor__(self, other: Predicate) -> "predicate":
        def _xor(*args: Any, **kwargs: Any) -> bool:
            return other(*args, **kwargs) ^ self.func(*args, **kwargs)

        _xor.__name__ = f"{_callable_name(other)}_xor_{self.__name__}"
        return predicate(_xor)

    def __invert__(self) -> "predicate":
        def _not(*args: Any, **kwargs: Any) -> bool:
            return not self.func(*args, **kwargs)

        _not.__name__ = f"not_{self.__name__}"
        return predicate(_not)

    def __repr__(self) -> str:
        return f"predicate({self.__name__})"


always_false = predicate(constant(False))
always_false.__doc__ = "A predicate that always returns False"
always_true = predicate(constant(True))
always_true.__doc__ = "A predicate that always returns True"


def all_pass(*predicates: Predicate) -> Predicate:
    """Return a predicate that is true only when all predicates pass."""

    def _all_pass(*args: Any, **kwargs: Any) -> bool:
        return all(predicate_(*args, **kwargs) for predicate_ in predicates)

    _all_pass.__name__ = "all_pass_" + "_".join(_callable_name(pred) for pred in predicates)
    return _all_pass


def any_pass(*predicates: Predicate) -> Predicate:
    """Return a predicate that is true when any predicate passes."""

    def _any_pass(*args: Any, **kwargs: Any) -> bool:
        return any(predicate_(*args, **kwargs) for predicate_ in predicates)

    _any_pass.__name__ = "any_pass_" + "_".join(_callable_name(pred) for pred in predicates)
    return _any_pass


def none_pass(*predicates: Predicate) -> Predicate:
    """Return a predicate that is true when no predicate passes."""

    def _none_pass(*args: Any, **kwargs: Any) -> bool:
        return not any(predicate_(*args, **kwargs) for predicate_ in predicates)

    _none_pass.__name__ = "none_pass_" + "_".join(_callable_name(pred) for pred in predicates)
    return _none_pass


def complement(predicate_: Predicate) -> Predicate:
    """Return a predicate that negates ``predicate_``."""

    def _complement(*args: Any, **kwargs: Any) -> bool:
        return not predicate_(*args, **kwargs)

    _complement.__name__ = f"not_{_callable_name(predicate_)}"
    return _complement


__all__ = [
    "predicate",
    "always_true",
    "always_false",
    "all_pass",
    "any_pass",
    "none_pass",
    "complement",
]
