# Hash Tables and Hash Maps

## What is a Hash Table?

A hash table (hash map) stores key-value pairs enabling O(1) average case lookup, insertion, and deletion.

Uses hash function to compute index from key. Store value at that index in underlying array.

## Hash Functions

Hash function converts key to array index: hash(key) → index.

Good hash functions distribute keys uniformly across array to minimize collisions.

Python's hash() function works for immutable types (int, str, tuple). Returns integer hash value.

## Python Dictionaries

Python dict is a hash table. Keys must be hashable (immutable and have __hash__ method).

```python
ages = {"Alice": 30, "Bob": 25}
ages["Alice"]  # O(1) lookup
ages["Charlie"] = 35  # O(1) insertion
del ages["Bob"]  # O(1) deletion
```

Dictionary operations are O(1) average case, O(n) worst case (with many collisions).

## Sets as Hash Tables

Python set stores unique elements using hash table. No values, just keys.

```python
seen = set()
seen.add(5)  # O(1)
if 5 in seen:  # O(1)
    pass
```

Sets useful for membership testing and removing duplicates.

## Collision Handling

Collision occurs when two keys hash to same index. Hash tables must handle collisions.

Chaining: each array slot holds linked list of key-value pairs with same hash.

Open addressing: if slot occupied, probe for next empty slot using sequence.

Python uses open addressing with random probing for dicts.

## Hash Table Size

Hash tables dynamically resize when load factor (items/capacity) exceeds threshold.

Resize creates larger array and rehashes all existing keys. Amortized O(1) insertion due to infrequent resizing.

## Time Complexity

Average case: O(1) for lookup, insert, delete.

Worst case: O(n) when all keys collide and form linked list or cause linear probing.

Good hash functions and dynamic resizing keep average case O(1) in practice.

## Space Complexity

Hash tables use O(n) space for n key-value pairs plus array overhead.

Trade space for time: extra memory enables constant-time operations.

## Common Hash Table Patterns

- Counting frequency: `char_count[c] = char_count.get(c, 0) + 1`
- Checking duplicates: add to set, if already present it's duplicate
- Two sum: store complements in dict for O(n) solution
- Grouping anagrams: sorted string as key, group words as value
- Caching results: memoization with dict

## Hash Table vs Array

Array: O(1) access by index, O(n) search by value, continuous memory.

Hash table: O(1) access by arbitrary key, keys need not be integers, scattered memory.

Use arrays when keys are small integers or order matters. Use hash tables for arbitrary keys or fast membership testing.

## When to Use Hash Tables

Use when:
- Need fast (O(1)) lookup by key
- Keys are hashable (immutable)
- Order doesn't matter (or use OrderedDict)
- Counting occurrences/frequencies
- Removing duplicates
- Checking membership

Hash tables are among most versatile data structures, enabling elegant O(n) solutions to many problems.

## Limitations

Keys must be immutable (lists can't be keys, tuples can).

No inherent ordering (though Python 3.7+ dicts maintain insertion order).

Space overhead compared to arrays.

Worst-case O(n) operations possible (rare with good hashing).
