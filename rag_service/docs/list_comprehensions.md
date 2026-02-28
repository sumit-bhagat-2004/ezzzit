# List Comprehensions in Python

## What are List Comprehensions?

List comprehensions provide concise syntax for creating lists. They combine iteration, optional filtering, and transformation in a single expression.

## Basic Syntax

```python
[expression for item in iterable]
```

This creates a new list by applying expression to each item:

```python
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
```

Equivalent to:
```python
squares = []
for x in range(5):
    squares.append(x**2)
```

## With Filtering

Add `if` condition to filter items:

```python
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

Only items where condition is True are included.

## Transformation

The expression can transform items:

```python
names = ["alice", "bob", "charlie"]
upper_names = [name.upper() for name in names]  # ["ALICE", "BOB", "CHARLIE"]
```

## Multiple Iterables

Iterate over multiple sequences with nested comprehensions:

```python
pairs = [(x, y) for x in [1, 2] for y in ['a', 'b']]
# [(1,'a'), (1,'b'), (2,'a'), (2,'b')]
```

Leftmost loop is outermost, rightmost is innermost.

## Nested Lists

Process nested structures:

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flattened = [item for row in matrix for item in row]  # [1, 2, 3, 4, 5, 6]
```

## When to Use

List comprehensions are ideal when:
- Creating new lists from existing sequences
- Applying transformations to all items
- Filtering based on conditions
- The logic fits in one readable line

## Advantages

- More concise than loops
- Often faster than equivalent loop code
- Pythonic and readable for simple transformations
- Less boilerplate (no append calls)

## When to Avoid

Use regular loops if:
- Logic is complex (multiple conditions)
- Comprehension becomes hard to read
- Side effects beyond list creation are needed
- Debugging line-by-line would help

## Related Comprehensions

Similar syntax works for other collections:

- Set comprehension: `{x for x in items}`
- Dict comprehension: `{k: v for k, v in pairs}`
- Generator expression: `(x for x in items)` (memory efficient)
