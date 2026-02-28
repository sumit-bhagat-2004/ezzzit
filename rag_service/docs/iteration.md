# Iteration and Loops in Python

## What is Iteration?

Iteration means repeating a block of code multiple times. Python provides loop constructs that iterate over sequences or repeat until conditions are met.

## For Loops

For loops iterate over sequences (lists, strings, ranges):

```python
for item in [1, 2, 3]:
    print(item)
```

For each element in the sequence, the loop:
1. Assigns element to loop variable (item)
2. Executes loop body
3. Moves to next element

## Loop Variables

The loop variable takes on each sequential value:

```python
for i in range(5):
    print(i)  # prints 0, 1, 2, 3, 4
```

Loop variable persists after loop ends, holding the last value.

## Range Function

`range()` generates number sequences:

- `range(5)` produces 0, 1, 2, 3, 4
- `range(1, 6)` produces 1, 2, 3, 4, 5
- `range(0, 10, 2)` produces 0, 2, 4, 6, 8 (step of 2)

Range is memory-efficient - it generates values on demand, not storing entire sequence.

## While Loops

While loops repeat as long as condition remains True:

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

While loops:
1. Evaluate condition
2. If True, execute body then return to step 1
3. If False, exit loop

## Infinite Loops

While loops that never become False run forever:

```python
while True:
    command = input("Enter command: ")
    if command == "quit":
        break
```

Use `break` to exit infinite loops based on runtime conditions.

## Loop Control

- `break` - exit loop immediately
- `continue` - skip rest of iteration, proceed to next
- `else` - executes after loop completes normally (not broken)

## Enumerate

`enumerate()` provides both index and value when iterating:

```python
for index, value in enumerate(['a', 'b', 'c']):
    print(f"{index}: {value}")
```

Outputs: `0: a`, `1: b`, `2: c`

## Iteration Best Practices

- Use for loops when iteration count is known
- Use while loops when repeating until condition changes
- Prefer iterating directly over collections rather than using index manipulation
