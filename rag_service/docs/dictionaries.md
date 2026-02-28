# Python Dictionaries

## What are Dictionaries?

Dictionaries are unordered collections of key-value pairs. They map keys to values, enabling fast lookups by key. Dictionaries are mutable and store unique keys.

## Dictionary Creation

Create dictionaries using curly braces with key:value pairs:

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}
scores = {"math": 95, "science": 88}
empty = {}
```

Keys must be immutable types (strings, numbers, tuples). Values can be any type.

## Accessing Values

Access values using bracket notation with keys:

```python
person = {"name": "Alice", "age": 30}
name = person["name"]    # "Alice"
age = person["age"]      # 30
```

Accessing non-existent key raises KeyError. Use `.get()` for safe access:

```python
city = person.get("city", "Unknown")  # returns "Unknown" if key missing
```

## Adding and Modifying

Add or modify entries by assignment:

```python
person["email"] = "alice@example.com"  # add new key
person["age"] = 31                     # modify existing value
```

## Dictionary Operations

- `len(dict)` - number of key-value pairs
- `key in dict` - check if key exists
- `dict.keys()` - get all keys
- `dict.values()` - get all values
- `dict.items()` - get key-value pairs
- `dict.update(other)` - merge another dictionary
- `del dict[key]` - remove key-value pair

## Iterating Dictionaries

Iterate through keys, values, or both:

```python
for key in person:
    print(key)

for key, value in person.items():
    print(f"{key}: {value}")
```

## Use Cases

Dictionaries excel at:
- Storing structured data (records, objects)
- Counting occurrences
- Caching computed results
- Representing mappings and associations

## Dictionary Comprehensions

Create dictionaries using comprehension syntax:

```python
squares = {x: x**2 for x in range(5)}  # {0:0, 1:1, 2:4, 3:9, 4:16}
```
