# Call Stack and Stack Frames

## What is the Call Stack?

The call stack is a data structure that tracks function calls. It's a stack (Last-In-First-Out) of stack frames, where each frame represents one active function call.

## Stack Frames

Each function call creates a stack frame containing:
- Function's local variables
- Function parameters
- Return address (where to continue after function returns)
- Call site information

When a function returns, its stack frame is removed (popped) from the stack.

## Stack Execution Flow

```python
def first():
    x = 1
    second()
    print("back in first")

def second():
    y = 2
    third()
    print("back in second")

def third():
    z = 3
    print("in third")

first()
```

Stack progression:
1. [first] - first() called
2. [first, second] - second() called from first
3. [first, second, third] - third() called from second
4. [first, second] - third() returns, frame popped
5. [first] - second() returns
6. [] - first() returns, stack empty

## Stack Depth

Stack depth is the number of active function calls. Each nested call increases depth by one.

Deeply recursive functions can cause stack overflow if depth exceeds system limits (typically thousands of frames).

## Stack Visualization

When A calls B which calls C:

```
[Top]
C's frame (local vars, return to B)
B's frame (local vars, return to A)  
A's frame (local vars, return to caller)
[Bottom]
```

Execution is always in the topmost frame. Returning removes that frame.

## Stack Trace

When errors occur, Python prints a stack trace showing the call stack from bottom to top, helping identify where the error originated and how execution got there.

## Recursion and the Stack

Recursive functions add multiple frames of the same function:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

factorial(3)
```

Stack for factorial(3):
- [factorial(3)]
- [factorial(3), factorial(2)]
- [factorial(3), factorial(2), factorial(1)]
- Returns unwind: 1 → 2 → 6

## Stack Memory

Stack frames use memory. Each call consumes stack space. Unbounded recursion causes stack overflow errors when memory is exhausted.
