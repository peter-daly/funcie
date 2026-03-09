# API

## `funcie.core`

### `identity(val)`

Returns the value passed in unchanged.

### `constant(val)`

Returns a callable that always returns `val`.

## Combinators

Basic composition examples:

```python
from funcie import compose, pipe

add1 = lambda x: x + 1
mul2 = lambda x: x * 2

assert compose(add1, mul2)(3) == 7  # add1(mul2(3))
assert pipe(add1, mul2)(3) == 8     # mul2(add1(3))
```

### `composable(func)`

Callable wrapper with operator composition:

- `a >> b`: pipe `a` into `b`
- `a << b`: compose `a` after `b`
- `a @ b`: juxt both on the same args, returns `(a_result, b_result)`

```python
from funcie import composable

inc = composable(lambda x: x + 1)
double = composable(lambda x: x * 2)

assert (inc >> double)(3) == 8
assert (double << inc)(3) == 8
assert (inc @ double)(3) == (4, 6)
```

### `compose(*funcs)`

Composes functions right-to-left.

```python
from funcie import compose

add1 = lambda x: x + 1
mul2 = lambda x: x * 2

assert compose(add1, mul2)(3) == 7
```

### `pipe(*funcs)`

Composes functions left-to-right.

```python
from funcie import pipe

add1 = lambda x: x + 1
mul2 = lambda x: x * 2

assert pipe(add1, mul2)(3) == 8
```

### `juxt(*funcs)`

Applies each function to the same input and returns a tuple of results.

### `flip(func)`

Returns a wrapper that swaps the first two positional arguments.

### `tap(side_effect)`

Runs a side-effect function and returns the original value.

## Currying

### `curry_n(n, func)`

Returns a curried positional wrapper up to arity `n`.

### `curry(func)`

Infers arity from required positional parameters and curries the function.

### `curried(func=None, *, n=None)`

Decorator form for currying:

- `@curried` uses `curry`
- `@curried(n=...)` uses `curry_n`

```python
from funcie import curried

@curried
def add(a, b, c):
    return a + b + c

assert add(1)(2)(3) == 6
```

## Collections

All collection helpers are lazy by default except `fold`.

### `keep(pred, iterable)` / `reject(pred, iterable)`

Lazy filter and inverse filter.

### `flat_map(func, iterable)`

Lazy map + flatten.

### `take(n, iterable)` / `drop(n, iterable)`

Lazy slice helpers.

### `partition(pred, iterable)`

Returns `(matched_iter, unmatched_iter)`.

### `fold(func, iterable, initial=...)`

Reduction helper.

```python
from funcie import keep

values = keep(lambda x: x % 2 == 0, range(6))
assert list(values) == [0, 2, 4]
```

## `funcie.predicate`

### `predicate`

A callable wrapper for boolean functions with operator-based composition:

- `p1 & p2`: logical and
- `p1 | p2`: logical or
- `p1 ^ p2`: logical xor
- `~p1`: logical not

Basic predicate examples:

```python
from funcie import predicate

is_even = predicate(lambda n: n % 2 == 0)
is_positive = predicate(lambda n: n > 0)

assert is_even(4) is True
assert is_even(5) is False
assert is_positive(10) is True
```

Combining predicates with logic operators:

```python
from funcie import predicate

is_even = predicate(lambda n: n % 2 == 0)
is_positive = predicate(lambda n: n > 0)

is_positive_even = is_even & is_positive
is_positive_or_even = is_even | is_positive
is_positive_xor_even = is_even ^ is_positive
is_odd = ~is_even

assert is_positive_even(4) is True
assert is_positive_even(-2) is False

assert is_positive_or_even(-2) is True
assert is_positive_or_even(-3) is False

assert is_positive_xor_even(-2) is True
assert is_positive_xor_even(4) is False

assert is_odd(5) is True
assert is_odd(4) is False
```

### Predicate helpers

- `all_pass(*preds)`
- `any_pass(*preds)`
- `none_pass(*preds)`
- `complement(pred)`

### `always_true` / `always_false`

Convenience predicates that always return `True` or `False`.
