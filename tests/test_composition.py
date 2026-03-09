import pytest

from funcie.composition import composable, compose, flip, juxt, pipe, tap


def test_compose_order_and_kwargs_forwarding():
    def annotate(value: int, *, suffix: str) -> str:
        return f"{value}{suffix}"

    composed = compose(str.upper, annotate)

    assert composed(10, suffix="x") == "10X"


def test_pipe_order_and_kwargs_forwarding():
    def annotate(value: int, *, suffix: str) -> str:
        return f"{value}{suffix}"

    piped = pipe(annotate, str.upper)

    assert piped(10, suffix="x") == "10X"


def test_compose_and_pipe_require_functions():
    with pytest.raises(ValueError):
        compose()

    with pytest.raises(ValueError):
        pipe()


def test_juxt_runs_all_functions_with_same_input():
    combined = juxt(lambda x: x + 1, lambda x: x * 2, str)

    assert combined(3) == (4, 6, "3")


def test_flip_swaps_first_two_arguments():
    def divide(a: int, b: int) -> float:
        return a / b

    flipped = flip(divide)

    assert flipped(2, 10) == 5.0


def test_flip_requires_two_positionals():
    def pair(a: int, b: int) -> tuple[int, int]:
        return a, b

    flipped = flip(pair)

    with pytest.raises(TypeError):
        flipped(1)


def test_tap_returns_original_value_after_side_effect():
    calls: list[int] = []

    def record(value: int) -> None:
        calls.append(value)

    tapped = tap(record)

    assert tapped(7) == 7
    assert calls == [7]


def test_composable_pipe_and_compose_operators():
    add1 = composable(lambda x: x + 1)
    mul2 = composable(lambda x: x * 2)

    piped = add1 >> mul2
    composed = mul2 << add1

    assert piped(3) == 8
    assert composed(3) == 8


def test_composable_works_with_plain_callables_on_either_side():
    inc = composable(lambda x: x + 1)

    assert (inc >> str)(3) == "4"
    assert ((lambda x: x * 2) >> composable(str))(3) == "6"
    assert (str << inc)(3) == "4"
    assert (inc @ str)(3) == (4, "3")
    assert ((lambda x: x * 2) @ inc)(3) == (6, 4)


def test_composable_matmul_operator_for_juxt():
    add1 = composable(lambda x: x + 1)
    mul2 = composable(lambda x: x * 2)

    juxted = add1 @ mul2

    assert juxted(3) == (4, 6)


def test_composable_rejects_non_callable_operands():
    inc = composable(lambda x: x + 1)

    with pytest.raises(TypeError):
        _ = inc >> 1

    with pytest.raises(TypeError):
        _ = inc << 1

    with pytest.raises(TypeError):
        _ = inc @ 1
