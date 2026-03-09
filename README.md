# funcie

`funcie` is a focused Python library of functional programming helpers.

## What you get

- Function composition: `compose`, `pipe`, `composable`
- Predicate composition: `predicate` with `&`, `|`, `^`, `~`
- Predicate helpers: `all_pass`, `any_pass`, `none_pass`, `complement`
- Currying: `curry`, `curry_n`, `curried`
- Collection helpers: `keep`, `reject`, `flat_map`, `take`, `drop`, `partition`, `fold`

## Install

```bash
uv sync --group dev
```

## Quick examples

### Composition

```python
from funcie import compose, pipe, composable

add1 = lambda x: x + 1
mul2 = lambda x: x * 2

assert compose(add1, mul2)(3) == 7
assert pipe(add1, mul2)(3) == 8

c_add1 = composable(add1)
c_mul2 = composable(mul2)
assert (c_add1 >> c_mul2)(3) == 8
assert (c_add1 @ c_mul2)(3) == (4, 6)
```

### Predicates

```python
from funcie import predicate

is_even = predicate(lambda n: n % 2 == 0)
is_positive = predicate(lambda n: n > 0)

is_positive_even = is_even & is_positive
is_odd = ~is_even

assert is_positive_even(4) is True
assert is_positive_even(-2) is False
assert is_odd(5) is True
```

### Currying

```python
from funcie import curried

@curried
def add(a, b, c):
    return a + b + c

assert add(1)(2)(3) == 6
```

## Development

```bash
make ci
```
