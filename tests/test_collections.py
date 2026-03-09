import pytest

from funcie.collections import drop, flat_map, fold, keep, partition, reject, take


def test_keep_reject_and_flat_map():
    values = [1, 2, 3, 4]

    assert list(keep(lambda x: x % 2 == 0, values)) == [2, 4]
    assert list(reject(lambda x: x % 2 == 0, values)) == [1, 3]
    assert list(flat_map(lambda x: (x, x * 10), [1, 2, 3])) == [1, 10, 2, 20, 3, 30]


def test_take_and_drop():
    values = [1, 2, 3, 4, 5]

    assert list(take(3, values)) == [1, 2, 3]
    assert list(drop(2, values)) == [3, 4, 5]

    with pytest.raises(ValueError):
        list(take(-1, values))

    with pytest.raises(ValueError):
        list(drop(-1, values))


def test_partition_returns_independent_iterators():
    matched, unmatched = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])

    assert list(matched) == [2, 4]
    assert list(unmatched) == [1, 3, 5]


def test_fold_behaviors():
    assert fold(lambda acc, x: acc + x, [1, 2, 3]) == 6
    assert fold(lambda acc, x: acc + x, [1, 2, 3], 10) == 16

    with pytest.raises(TypeError):
        fold(lambda acc, x: acc + x, [])
