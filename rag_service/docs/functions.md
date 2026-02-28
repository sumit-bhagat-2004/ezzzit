# Python Functions

## What are Functions?

Functions are reusable blocks of code that perform specific tasks. They accept inputs (parameters), execute statements, and optionally return outputs.

## Function Definition

Define functions using the `def` keyword:

```python
def greet(name):
    message = f"Hello, {name}"
    return message
```

Function definition includes:
- Function name
- Parameter list in parentheses
- Colon and indented body
- Optional return statement

## Function Calls

Call a function by writing its name followed by arguments in parentheses:

```python
result = greet("Alice")
```

When called, execution jumps to the function definition, executes its body, then returns to the call site.

## Parameters and Arguments

Parameters are variable names in function definition. Arguments are actual values passed during function call.

```python
def add(a, b):  # a and b are parameters
    return a + b

sum_val = add(3, 5)  # 3 and 5 are arguments
```

## Return Statement

The `return` statement sends a value back to the caller and exits the function:

```python
def square(x):
    return x * x

result = square(4)  # result gets value 16
```

Without a return statement, functions return `None` by default.

## Scope

Variables defined inside functions are local - they only exist within that function. Variables outside functions are global.

```python
x = 10  # global

def modify():
    y = 5  # local to modify()
    return y

print(x)  # accessible
print(y)  # error - y doesn't exist here
```

## Call Stack

Each function call adds a frame to the call stack. When the function returns, its frame is removed. The stack tracks:
- Current execution point
- Local variables
- Return address

Nested function calls build up stack frames, unwinding as each returns.

## Function Arguments

Functions support various argument patterns:

- Positional: matched by order
- Keyword: matched by name
- Default values: used if not provided
- Variable arguments: `*args` and `**kwargs`
