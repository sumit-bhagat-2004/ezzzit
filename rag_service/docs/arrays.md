# Arrays and Lists in Programming

Arrays and lists are fundamental data structures that store collections of elements. Understanding how to work with them efficiently is crucial for programming.

## Arrays vs Lists

In many languages, arrays and lists have distinct characteristics:

**Arrays:**
- Fixed size (in languages like Java, C++)
- Elements stored in contiguous memory
- Fast indexed access (O(1))
- All elements typically same type

**Lists (Python):**
- Dynamic size (can grow/shrink)
- Implemented as dynamic arrays
- Also O(1) for indexed access
- Can contain mixed types

In Python, we primarily work with lists, which provide array functionality with additional flexibility.

## Creating Arrays/Lists

Python offers multiple ways to create lists:

```python
# Empty list
empty_list = []

# List with values
numbers = [1, 2, 3, 4, 5]

# List comprehension
squares = [x**2 for x in range(10)]

# Using list() constructor
from_range = list(range(1, 6))
```

## Accessing Elements

### Indexing

Access elements using zero-based indexing:

```python
numbers = [10, 20, 30, 40, 50]
first = numbers[0]    # 10
third = numbers[2]    # 30
last = numbers[-1]    # 50 (negative indexing from end)
```

### Slicing

Extract sublists using slice notation:

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
subset = numbers[2:5]     # [2, 3, 4]
first_three = numbers[:3] # [0, 1, 2]
last_three = numbers[-3:] # [7, 8, 9]
every_second = numbers[::2] # [0, 2, 4, 6, 8]
```

## Modifying Lists

### Adding Elements

```python
numbers = [1, 2, 3]

# Append to end
numbers.append(4)  # [1, 2, 3, 4]

# Insert at position
numbers.insert(0, 0)  # [0, 1, 2, 3, 4]

# Extend with another list
numbers.extend([5, 6])  # [0, 1, 2, 3, 4, 5, 6]
```

### Removing Elements

```python
numbers = [1, 2, 3, 2, 4]

# Remove by value (first occurrence)
numbers.remove(2)  # [1, 3, 2, 4]

# Remove by index
del numbers[0]  # [3, 2, 4]

# Pop (remove and return)
last = numbers.pop()  # Returns 4, list becomes [3, 2]
```

## Common Array Operations

### Searching

```python
numbers = [10, 20, 30, 40, 50]

# Check if element exists
if 30 in numbers:
    print("Found")

# Find index
index = numbers.index(30)  # Returns 2

# Count occurrences
count = numbers.count(20)
```

### Sorting

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sort in place
numbers.sort()  # [1, 1, 2, 3, 4, 5, 6, 9]

# Return sorted copy
sorted_nums = sorted(numbers, reverse=True)

# Custom sorting
words = ['apple', 'pie', 'zoo', 'a']
words.sort(key=len)  # Sort by length
```

### Reversing

```python
numbers = [1, 2, 3, 4, 5]

# Reverse in place
numbers.reverse()  # [5, 4, 3, 2, 1]

# Return reversed copy
reversed_nums = list(reversed(numbers))
```

## Array Algorithms

### Linear Search

Search sequentially through array:

```python
def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1
```

### Binary Search

Efficient search in sorted arrays (O(log n)):

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### Two Pointer Technique

Efficient for many array problems:

```python
def reverse_array(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

## Multi-dimensional Arrays

### Creating 2D Arrays

```python
# Using list comprehension
matrix = [[0 for _ in range(3)] for _ in range(3)]

# Nested lists
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

### Accessing 2D Arrays

```python
element = matrix[1][2]  # Row 1, Column 2

# Iterating
for row in matrix:
    for value in row:
        print(value)
```

## Performance Considerations

### Time Complexity

- Access by index: O(1)
- Search (unsorted): O(n)
- Search (sorted): O(log n) with binary search
- Insert/Delete at end: O(1) amortized
- Insert/Delete at beginning: O(n)

### Space Optimization

```python
# Use generators for large sequences
large_nums = (x**2 for x in range(1000000))  # Doesn't create full list

# Use array module for homogeneous numeric data
import array
int_array = array.array('i', [1, 2, 3, 4, 5])  # More memory efficient
```

## Best Practices

1. Use list comprehensions for transformations
2. Avoid modifying lists while iterating over them
3. Use appropriate data structure (set for membership testing, deque for queue operations)
4. Consider NumPy for numerical computations
5. Pre-allocate size when possible for performance
6. Use slicing instead of manual loops when possible
7. Remember that lists are mutable (can cause unexpected behavior)

## Common Patterns

### Filtering

```python
# Filter even numbers
evens = [x for x in numbers if x % 2 == 0]
```

### Mapping

```python
# Square all numbers
squares = [x**2 for x in numbers]
```

### Accumulation

```python
# Running sum
total = sum(numbers)
```

### Pairing

```python
# Combine two lists
pairs = list(zip(list1, list2))
```