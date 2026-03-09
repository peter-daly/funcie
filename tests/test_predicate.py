from funcie.predicate import all_pass, any_pass, complement, none_pass, predicate


def test_name():
    def f():
        return True

    def g():
        return True

    p1 = predicate(f)
    p2 = predicate(g)

    assert p1.__name__ == "f"
    assert p2.__name__ == "g"


def test_logic_operations():
    def f():
        return True

    def g():
        return False

    pf = predicate(f)
    pg = predicate(g)

    pand = pf & pg
    por = pf | pg
    pxor = pf ^ pg
    pinv = ~pf

    assert pand() is False
    assert por() is True
    assert pxor() is True
    assert pinv() is False

    assert pand.__name__ == "f_and_g"
    assert por.__name__ == "f_or_g"
    assert pxor.__name__ == "f_xor_g"
    assert pinv.__name__ == "not_f"


def test_predicate_combinators():
    def is_even(value: int) -> bool:
        return value % 2 == 0

    def over_ten(value: int) -> bool:
        return value > 10

    both = all_pass(is_even, over_ten)
    either = any_pass(is_even, over_ten)
    neither = none_pass(is_even, over_ten)

    assert both(12) is True
    assert both(9) is False

    assert either(12) is True
    assert either(8) is True
    assert either(9) is False

    assert neither(9) is True
    assert neither(8) is False

    is_odd = complement(is_even)
    assert is_odd(3) is True
    assert is_odd(2) is False
