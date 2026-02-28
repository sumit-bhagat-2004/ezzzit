# Nested Loops in Python

## What are Nested Loops?

Nested loops occur when one loop is placed inside another loop's body. The inner loop executes completely for each iteration of the outer loop.

## Basic Structure

```python
for i in range(3):
    for j in range(2):
        print(f"i={i}, j={j}")
```

Output shows inner loop (j) completes all iterations before outer loop (i) advances.

## Execution Pattern

For nested loops with outer loop of N iterations and inner loop of M iterations:
- Inner loop executes N × M times total
- Each outer iteration triggers complete inner loop cycle

Example with range(3) outer and range(2) inner:
- i=0: j iterates 0, 1
- i=1: j iterates 0, 1
- i=2: j iterates 0, 1
Total: 6 iterations

## Matrix Processing

Nested loops naturally handle 2D structures like matrices:

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in matrix:
    for element in row:
        print(element, end=" ")
    print()  # newline after each row
```

Outer loop processes rows, inner loop processes elements within each row.

## Nested Iteration Depth

Loops can nest to any depth, though deep nesting becomes harder to understand:

```python
for i in range(2):
    for j in range(2):
        for k in range(2):
            print(i, j, k)
```

Three levels deep produces 2³ = 8 combinations.

## Performance Considerations

Time complexity multiplies with nesting:
- Single loop: O(n)
- Nested two-deep: O(n²)
- Nested three-deep: O(n³)

Deeply nested loops over large ranges can be slow.

## Common Patterns

Nested loops commonly appear in:
- Grid/matrix traversal
- Comparing all pairs of items
- Generating combinations
- Multi-dimensional processing
- Pattern printing (stars, pyramids)

## Breaking Nested Loops

`break` only exits the innermost loop containing it. To exit multiple levels, use flags or exceptions:

```python
found = False
for i in range(10):
    for j in range(10):
        if condition:
            found = True
            break
    if found:
        break
```
