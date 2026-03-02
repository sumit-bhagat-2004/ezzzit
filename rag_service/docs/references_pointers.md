# Pointers and References in Python

## References in Python

Python doesn't have traditional pointers like C/C++. Instead, variables hold references to objects. A reference is like an arrow pointing to an object in memory.

Assignment creates references, not copies. When you write `b = a`, both variables reference the same object.

## Understanding Object Identity

Every object has a unique identity (memory address). The `id()` function returns this address.

```python
a = [1, 2, 3]
b = a
print(id(a) == id(b))  # True - same object
```

The `is` operator checks if two variables reference the same object (same identity).

## Reference Reassignment

Reassigning a variable makes it reference a different object. The original object is unchanged if other references exist.

```python
a = [1, 2, 3]
b = a        # b references same list
a = [4, 5]   # a now references different list
```

After reassignment, a and b reference different objects. Changes to one don't affect the other.

## Mutable Object Sharing

When multiple variables reference the same mutable object (list, dict), changes through one variable affect all references.

```python
a = [1, 2]
b = a
b.append(3)  # modifies shared list
print(a)     # [1, 2, 3]
```

This is called aliasing. All aliases see the same object's state.

## None as Null Reference

`None` represents the absence of an object. It's Python's null reference, often used to indicate "no value" or "end of list".

```python
next_node = None  # no next element
```

Checking `if node is None:` safely detects missing references before dereferencing.

## Reference Counting

Python uses reference counting for memory management. Each object tracks how many references point to it.

When reference count drops to zero, the object is garbage collected and memory is freed.

Creating a reference increments count. Deleting reference or reassigning variable decrements count.

## Function Arguments Pass by Reference

Python passes object references to functions, not copies. Functions receive references to the same objects.

Inside a function, you can modify mutable objects (lists, dicts) and changes persist outside the function.

Reassigning a parameter variable inside a function doesn't affect the original. It just changes what that local variable references.

## Copying vs Referencing

Assignment (b = a) creates a new reference to the same object.

Shallow copy (b = a.copy()) creates a new object with references to same inner objects.

Deep copy (import copy; b = copy.deepcopy(a)) recursively copies all nested objects.

## Circular References

Objects can reference each other in cycles. Linked list nodes reference other nodes, forming chains.

```python
node1.next = node2
node2.next = node3
node3.next = node1  # circular
```

Python's garbage collector handles circular references that aren't reachable from root.
