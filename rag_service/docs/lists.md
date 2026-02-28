# Python Lists

## What are Lists?

Lists are ordered, mutable collections that store sequences of items. Lists can contain elements of different types and allow duplicates.

## List Creation

Create lists using square brackets:

```python
numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]
mixed = [1, "hello", 3.14, True]
empty = []
```

## List Indexing

Access elements by position using zero-based indexing:

```python
fruits = ["apple", "banana", "cherry"]
first = fruits[0]   # "apple"
second = fruits[1]  # "banana"
last = fruits[-1]   # "cherry" (negative indexes count from end)
```

## List Slicing

Extract sublists using slice notation `[start:end]`:

```python
numbers = [0, 1, 2, 3, 4, 5]
subset = numbers[1:4]  # [1, 2, 3]
first_three = numbers[:3]  # [0, 1, 2]
last_two = numbers[-2:]  # [4, 5]
```

Slices include start index, exclude end index.

## List Mutability

Lists are mutable - you can change their contents after creation:

```python
items = [1, 2, 3]
items[0] = 10      # modify element
items.append(4)    # add to end
items.insert(1, 5)  # insert at position
items.remove(2)    # remove by value
```

## Common List Operations

- `len(list)` - get number of elements
- `list.append(x)` - add item to end
- `list.extend(other)` - add all items from other list
- `list.pop()` - remove and return last item
- `list.sort()` - sort in place
- `item in list` - check membership

## List Iteration

Iterate through list elements:

```python
for item in items:
    print(item)
```

## List Comprehensions

Create lists using compact syntax:

```python
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
evens = [x for x in numbers if x % 2 == 0]
```

List comprehensions combine iteration, filtering, and transformation.
