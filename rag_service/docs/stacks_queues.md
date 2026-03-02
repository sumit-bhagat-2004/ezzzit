# Stacks and Queues in Python

## What is a Stack?

A stack is a Last-In-First-Out (LIFO) data structure. The last element added is the first one removed.

Think of a stack of plates: you add plates on top and remove from the top. You can't access plates in the middle without removing everything above.

## Stack Operations

- Push: add element to top, O(1)
- Pop: remove and return top element, O(1)
- Peek: view top element without removing, O(1)
- IsEmpty: check if stack is empty, O(1)

All operations work at one end (the top) making them constant time.

## Implementing Stacks

Python lists work well as stacks. Use append() for push and pop() for pop.

```python
stack = []
stack.append(1)  # push
stack.append(2)
top = stack.pop()  # pop returns 2
```

List append and pop at the end are O(1) operations, perfect for stack behavior.

## Stack Use Cases

Stacks are used for:
- Function call stack (recursion tracking)
- Undo/redo operations
- Expression evaluation (reverse Polish notation)
- Backtracking algorithms (maze solving, DFS)
- Syntax parsing (matching brackets)

The LIFO property means most recent items are processed first.

## What is a Queue?

A queue is a First-In-First-Out (FIFO) data structure. The first element added is the first one removed.

Think of a line of people: new arrivals join the back, service happens at the front. Fair ordering is maintained.

## Queue Operations

- Enqueue: add element to back, O(1)
- Dequeue: remove and return front element, O(1)
- Front: view front element without removing, O(1)
- IsEmpty: check if queue is empty, O(1)

Elements enter at one end (rear) and exit at the other (front).

## Implementing Queues

Use collections.deque (double-ended queue) for efficient queues. Lists work but dequeue is slow.

```python
from collections import deque
queue = deque()
queue.append(1)      # enqueue
front = queue.popleft()  # dequeue
```

deque provides O(1) append and popleft operations. List pop(0) is O(n) due to shifting.

## Queue Use Cases

Queues are used for:
- Task scheduling (first come, first served)
- Breadth-first search (BFS)
- Print job spooling
- Message buffering
- Request handling in servers

The FIFO property ensures fair processing order.

## Deque (Double-Ended Queue)

A deque allows insertion and deletion at both ends, all in O(1) time.

```python
from collections import deque
dq = deque()
dq.append(1)      # add to right
dq.appendleft(0)  # add to left
dq.pop()          # remove from right
dq.popleft()      # remove from left
```

Deques can function as both stacks and queues, combining their capabilities.

## Priority Queue

A priority queue removes elements by priority, not insertion order. The highest priority element is dequeued first.

Implemented with heaps, priority queues provide O(log n) insertion and O(log n) removal of highest priority element.

Use heapq module in Python for priority queues.

## Stack vs Queue

Stack: LIFO, most recent first. Used when order of processing should be reversed from arrival order.

Queue: FIFO, oldest first. Used when fair ordering must be preserved, processing in arrival order.

Choice depends on whether you need most-recent-first or first-come-first-served behavior.
