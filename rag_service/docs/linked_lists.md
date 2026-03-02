# Linked Lists in Python

## What are Linked Lists?

A linked list is a linear data structure where elements (called nodes) are not stored in contiguous memory locations. Each node contains data and a reference (pointer) to the next node in the sequence.

## Node Structure

A basic node contains two parts:
- Data: the value stored in the node
- Next: reference to the next node

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

Each node object stores its value in `data` and a reference to the next node in `next`. The last node's `next` is `None`.

## Linked List vs Array

Arrays store elements contiguously in memory with O(1) index access. Linked lists store elements in scattered memory locations connected by references.

Linked lists allow O(1) insertion/deletion at known positions (just change references). Arrays require O(n) shifting for insertions/deletions in the middle.

Arrays provide O(1) random access by index. Linked lists require O(n) traversal to access the nth element.

## Traversing a Linked List

Start from head node and follow next references until reaching None:

```python
current = head
while current is not None:
    process(current.data)
    current = current.next
```

Time complexity: O(n) where n is number of nodes.

## Reversing a Linked List

Reversing requires changing the direction of all next pointers. Use three pointers: previous, current, and next.

Algorithm:
1. Initialize prev = None, current = head
2. While current is not None:
   - Save next node (temp = current.next)
   - Reverse current's pointer (current.next = prev)
   - Move prev and current forward (prev = current, current = temp)
3. Return prev as new head

Time complexity: O(n), Space complexity: O(1).

The key insight is that you reverse one pointer at a time while maintaining references to avoid losing the rest of the list.

## Linked List Operations

- Insert at head: O(1) - create new node, point it to current head
- Insert at tail: O(n) - traverse to end, add new node
- Delete node: O(n) - find node, adjust previous node's next pointer
- Search: O(n) - traverse until finding value or reaching end
- Get length: O(n) - count nodes by traversal

## Types of Linked Lists

Singly Linked List: each node points only to next node. Can only traverse forward.

Doubly Linked List: each node has both next and prev pointers. Allows bidirectional traversal. Requires more memory but enables O(1) deletion when node reference is known.

Circular Linked List: last node points back to head instead of None. Useful for round-robin scheduling.

## Memory and References

Linked list nodes are dynamically allocated objects in Python. Each node occupies memory for data plus reference pointer (typically 8 bytes on 64-bit systems).

When you change node.next, you're reassigning a reference, not moving data. The actual node objects don't move in memory.

Deleting a node means removing references to it. Python's garbage collector reclaims memory when no references remain.
