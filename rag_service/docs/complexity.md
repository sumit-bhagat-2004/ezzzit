# Time Complexity Intuition

## What is Time Complexity?

Time complexity describes how runtime grows as input size increases. It helps predict performance and compare algorithm efficiency.

## Big O Notation

Big O expresses complexity in terms of input size n:

- O(1) - Constant: same time regardless of input size
- O(log n) - Logarithmic: doubles input, adds one step
- O(n) - Linear: doubles input, doubles time
- O(n log n) - Log-linear: efficient sorting
- O(n²) - Quadratic: nested loops over data
- O(2ⁿ) - Exponential: recursive branching

## Constant Time O(1)

Operations that take same time regardless of data size:

```python
arr[5] = 10        # array access
dict[key] = value  # dictionary insert/lookup (average)
x = a + b          # arithmetic
```

## Linear Time O(n)

Time grows proportionally with input size:

```python
for item in items:  # one pass through n items
    print(item)     # O(n)

sum(numbers)        # O(n) - must visit all n elements
```

## Quadratic Time O(n²)

Nested iteration over same data:

```python
for i in range(n):
    for j in range(n):  # inner loop runs n times for each outer iteration
        print(i, j)     # n × n = n² operations
```

Common in comparing all pairs or nested processing.

## Counting Operations

Focus on operations that scale with input:

```python
result = 0                # O(1)
for i in range(n):        # loop n times
    result += arr[i]      # O(1) per iteration
# Total: O(n)
```

Constants and lower-order terms are ignored: O(3n + 5) simplifies to O(n).

## Best, Average, Worst Case

Algorithms may perform differently based on input:

- Best case: optimal input arrangement
- Average case: typical expected performance
- Worst case: unfavorable input (usually analyzed)

## Space Complexity

Similar to time but measures memory usage:

```python
arr = [0] * n     # O(n) space
matrix = [[0] * n for _ in range(n)]  # O(n²) space
```

## Comparison

From fastest to slowest growth:
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)

For large inputs, complexity dominates performance.

## Practical Impact

- O(n): scales to millions of items
- O(n²): struggles beyond thousands
- O(2ⁿ): only works for small inputs (n < 20-30)

## Optimization Goal

Reduce complexity when possible:
- O(n²) → O(n log n) using better algorithm
- O(n) → O(1) using hash tables for lookup
