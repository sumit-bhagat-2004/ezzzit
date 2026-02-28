# Python Variables and Assignment

## What are Variables?

Variables are named containers that store data values in memory. In Python, you don't need to declare variable types explicitly - the interpreter infers the type from the assigned value.

## Variable Assignment

Assignment uses the equals sign (=) operator. The value on the right side is stored in the variable name on the left side.

```python
x = 5           # integer
name = "Alice"  # string
score = 98.5    # float
is_valid = True # boolean
```

## Assignment Process

When you write `x = 5`, Python:
1. Evaluates the right side (the value 5)
2. Creates a reference from variable name 'x' to that value
3. Stores this binding in the current namespace

Variables are references to objects, not containers holding values. Multiple variables can reference the same object.

## Naming Rules

Variable names must:
- Start with a letter or underscore
- Contain only letters, numbers, and underscores
- Be case-sensitive (age and Age are different)
- Not use Python keywords

## Multiple Assignment

Python supports assigning multiple variables in one line:

```python
a, b, c = 1, 2, 3
x = y = z = 0
```

## Dynamic Typing

Variables can be reassigned to different types:

```python
value = 42        # integer
value = "hello"   # now a string
```

The type is associated with the object, not the variable name.
