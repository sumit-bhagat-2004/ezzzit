# Exception Handling in Python

## What are Exceptions?

Exceptions are runtime errors that disrupt normal program flow. When errors occur, Python raises exception objects containing error information.

## Try-Except Blocks

Handle exceptions using try-except blocks:

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
    result = None
```

Code in `try` block executes normally. If an exception occurs, execution jumps to matching `except` block.

## Multiple Exception Types

Handle different exceptions separately:

```python
try:
    value = int(user_input)
    result = 100 / value
except ValueError:
    print("Invalid number format")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

Python checks except blocks in order, executing first match.

## Catching All Exceptions

Catch any exception with bare `except`:

```python
try:
    risky_operation()
except Exception as e:
    print(f"Error occurred: {e}")
```

Use cautiously - it's usually better to catch specific exceptions.

## Finally Block

`finally` executes regardless of whether exception occurred:

```python
try:
    file = open("data.txt")
    process(file)
except FileNotFoundError:
    print("File not found")
finally:
    file.close()  # always closes file
```

Finally is ideal for cleanup (closing files, releasing resources).

## Else Block

`else` executes only if try block succeeds (no exception):

```python
try:
    value = int(user_input)
except ValueError:
    print("Invalid input")
else:
    print(f"Successfully parsed: {value}")
```

## Raising Exceptions

Raise exceptions explicitly with `raise`:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Divisor cannot be zero")
    return a / b
```

## Exception Flow

When exception occurs:
1. Normal execution stops
2. Python searches for matching except handler
3. If found, handler executes
4. Finally block runs (if present)
5. Execution continues after try-except

If no handler matches, exception propagates to caller.

## Common Built-in Exceptions

- `ValueError` - inappropriate value
- `TypeError` - wrong type
- `KeyError` - invalid dictionary key
- `IndexError` - list index out of range
- `FileNotFoundError` - file doesn't exist
- `ZeroDivisionError` - division by zero
