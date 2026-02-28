# Python Scope and Namespaces

## What is Scope?

Scope determines where variables are accessible in code. Python uses lexical scoping - a variable's visibility depends on where it's defined in the source code structure.

## Scope Levels

Python has four scope levels (LEGB rule):

1. **Local** - variables inside current function
2. **Enclosing** - variables in outer functions (for nested functions)
3. **Global** - variables at module level
4. **Built-in** - Python's built-in names

Python searches these scopes in order when resolving variable names.

## Local Scope

Variables created inside a function are local to that function:

```python
def calculate():
    result = 42  # local variable
    return result

print(result)  # Error - result doesn't exist here
```

Local variables exist only during function execution. They're created when function is called and destroyed when it returns.

## Global Scope

Variables defined at module level (outside all functions) are global:

```python
count = 0  # global

def increment():
    global count
    count += 1  # modifies global count
```

Without `global` keyword, assignment creates a new local variable instead of modifying global one.

## Variable Shadowing

Local variables can have the same name as outer variables, shadowing them:

```python
x = 10  # global

def func():
    x = 5  # local x shadows global x
    print(x)  # prints 5

func()
print(x)  # prints 10
```

## Function Parameters

Function parameters are local variables. They're created when function is called and initialized with argument values:

```python
def process(data):  # data is local
    result = data * 2
    return result
```

## Scope and Memory

When a function returns, its local scope is destroyed and local variables are garbage collected (if no references remain).

## Nested Function Scopes

Inner functions can access variables from outer functions:

```python
def outer():
    x = 10
    def inner():
        print(x)  # accesses outer's x
    inner()
```

Use `nonlocal` keyword to modify enclosing scope variables.

## Global vs Local Best Practices

- Minimize global variable use
- Pass data through function parameters
- Return results rather than modifying globals
- Use local variables for temporary calculations
