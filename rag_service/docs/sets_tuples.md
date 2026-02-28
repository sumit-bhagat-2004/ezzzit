# Sets and Tuples in Python

## Sets

Sets are unordered collections of unique elements. They don't allow duplicates and don't maintain insertion order.

### Creating Sets

```python
colors = {"red", "green", "blue"}
numbers = {1, 2, 3, 3, 2}  # duplicates removed: {1, 2, 3}
empty = set()  # note: {} creates empty dict, not set
```

### Set Operations

- `add(x)` - add element
- `remove(x)` - remove element (error if not found)
- `discard(x)` - remove element (no error if not found)
- `x in set` - membership test (very fast)

```python
fruits = {"apple", "banana"}
fruits.add("cherry")
fruits.remove("banana")
```

### Mathematical Set Operations

Sets support mathematical operations:

- `a | b` or `a.union(b)` - elements in either set
- `a & b` or `a.intersection(b)` - elements in both sets
- `a - b` or `a.difference(b)` - elements in a but not b
- `a ^ b` or `a.symmetric_difference(b)` - elements in one but not both

### Set Use Cases

- Remove duplicates from list: `unique = list(set(items))`
- Fast membership testing
- Mathematical set operations
- Tracking seen items

## Tuples

Tuples are immutable ordered sequences, like read-only lists.

### Creating Tuples

```python
point = (3, 4)
single = (42,)  # note comma - (42) is just a number
empty = ()
```

### Tuple Features

Tuples support:
- Indexing: `point[0]` returns 3
- Slicing: `point[0:2]`
- Iteration: `for x in point:`
- Length: `len(point)`

But NOT:
- Modification: `point[0] = 5` raises error
- Append, remove, or other mutation

### Tuple Unpacking

Assign tuple elements to multiple variables:

```python
coordinates = (10, 20, 30)
x, y, z = coordinates  # x=10, y=20, z=30
```

Useful for returning multiple values from functions:

```python
def get_stats():
    return (42, 3.14, "result")

count, avg, label = get_stats()
```

### When to Use Tuples

- Data that shouldn't change (coordinates, RGB colors)
- Dictionary keys (must be immutable)
- Returning multiple values
- Slightly better performance than lists
- Signal immutability intent to readers
