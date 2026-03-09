import funcie

EXPECTED_EXPORTS = {
    "constant",
    "identity",
    "compose",
    "pipe",
    "juxt",
    "composable",
    "flip",
    "tap",
    "curried",
    "curry",
    "curry_n",
    "keep",
    "reject",
    "flat_map",
    "take",
    "drop",
    "partition",
    "fold",
    "predicate",
    "always_true",
    "always_false",
    "all_pass",
    "any_pass",
    "none_pass",
    "complement",
}


def test_top_level_exports_present_and_callable():
    exported = set(funcie.__all__)

    assert EXPECTED_EXPORTS.issubset(exported)

    for name in EXPECTED_EXPORTS:
        assert callable(getattr(funcie, name))
