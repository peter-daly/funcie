import pytest

from funcie.curry import curried, curry, curry_n


def test_curry_n_progressive_application():
    def add3(a: int, b: int, c: int) -> int:
        return a + b + c

    curried = curry_n(3, add3)

    assert curried(1)(2)(3) == 6
    assert curried(1, 2)(3) == 6
    assert curried(1)(2, 3) == 6
    assert curried(1, 2, 3) == 6


def test_curry_n_rejects_kwargs_and_empty_calls():
    def add2(a: int, b: int) -> int:
        return a + b

    curried = curry_n(2, add2)

    with pytest.raises(TypeError):
        curried(a=1)

    with pytest.raises(TypeError):
        curried()


def test_curry_n_requires_positive_n():
    with pytest.raises(ValueError):
        curry_n(0, lambda x: x)


def test_curry_inferrs_required_positional_arity():
    def mul(a: int, b: int) -> int:
        return a * b

    curried = curry(mul)

    assert curried(3)(4) == 12


def test_curry_rejects_unsupported_signatures():
    def with_varargs(*values: int) -> int:
        return sum(values)

    def with_required_kw(a: int, *, b: int) -> int:
        return a + b

    def with_defaults(a: int, b: int = 1) -> int:
        return a + b

    with pytest.raises(ValueError):
        curry(with_varargs)

    with pytest.raises(ValueError):
        curry(with_required_kw)

    with pytest.raises(ValueError):
        curry(with_defaults)


def test_curried_decorator_infers_arity():
    @curried
    def add3(a: int, b: int, c: int) -> int:
        """Add three numbers."""
        return a + b + c

    assert add3(1)(2)(3) == 6
    assert add3.__name__ == "add3"
    assert add3.__doc__ == "Add three numbers."


def test_curried_decorator_with_explicit_n():
    @curried(n=2)
    def mul(a: int, b: int, c: int) -> int:
        return a * b * c

    curried_mul = mul(2)
    assert callable(curried_mul)
    assert curried_mul(3, 4) == 24


def test_curried_decorator_carries():
    @curried()
    def add(a: int, b: int) -> int:
        return a + b

    add5 = add(5)
    assert add5(10) == 15

    assert add(1, 2) == 3
