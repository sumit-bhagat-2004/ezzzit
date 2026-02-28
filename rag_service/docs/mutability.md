# Mutability and References in Python

## What is Mutability?

Mutability determines whether an object's contents can be modified after creation. Python objects are either mutable (changeable) or immutable (unchangeable).

## Immutable Types

These types cannot be modified after creation:
- Numbers (int, float)
- Strings
- Tuples
- Frozen sets

Operations appear to modify them but actually create new objects:

```python
s = "hello"
s = s + " world"  # creates new string, doesn't modify original
```

## Mutable Types

These types can be modified in place:
- Lists
- Dictionaries
- Sets
- User-defined classes (by default)

```python
numbers = [1, 2, 3]
numbers.append(4)  # modifies existing list
```

## References and Assignment

Variables hold references to objects, not the objects themselves:

```python
a = [1, 2, 3]
b = a  # b references same list as a
b.append(4)
print(a)  # [1, 2, 3, 4] - a changed too!
```

Both variables point to the same object in memory.

## Object Identity

`is` operator checks if two variables reference the same object:

```python
a = [1, 2]
b = a
c = [1, 2]

print(a is b)  # True - same object
print(a is c)  # False - different objects (same content)
print(a == c)  # True - equal content
```

## Copying

Shallow copy creates new object but references may still be shared:

```python
import copy
original = [1, 2, [3, 4]]
shallow = original.copy()
shallow[2].append(5)  # modifies nested list in both
```

Deep copy recursively copies all nested objects:

```python
deep = copy.deepcopy(original)  # fully independent
```

## Function Arguments

Function parameters receive references to objects:

```python
def modify_list(lst):
    lst.append(4)  # modifies original list

numbers = [1, 2, 3]
modify_list(numbers)
print(numbers)  # [1, 2, 3, 4]
```

Reassigning parameter doesn't affect original:

```python
def reassign(lst):
    lst = [9, 9, 9]  # creates new list, doesn't affect original

numbers = [1, 2, 3]
reassign(numbers)
print(numbers)  # [1, 2, 3] - unchanged
```

## Mutable Default Arguments

Avoid mutable defaults - they persist across calls:

```python
def append_to(item, lst=[]):  # DON'T DO THIS
    lst.append(item)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - unexpected!
```

Use None as default instead:

```python
def append_to(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```
