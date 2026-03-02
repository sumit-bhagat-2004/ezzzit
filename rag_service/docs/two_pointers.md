# Two Pointers Pattern

## What is Two Pointers?

Two pointers is a technique using two array indices that traverse data, often from opposite ends or at different speeds.

Reduces nested loops from O(n²) to O(n) by intelligently moving pointers based on conditions.

## Opposite Direction Pointers

Start one pointer at beginning, another at end. Move them toward each other based on some condition.

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None
```

Time complexity: O(n) - each pointer moves at most n times.

Works when array is sorted and you need to find pairs meeting criteria.

## Same Direction Pointers

Both pointers move in same direction but at different speeds or for different purposes.

Useful for removing duplicates, partitioning, or sliding window problems.

```python
def remove_duplicates(arr):
    if not arr:
        return 0
    write = 1
    for read in range(1, len(arr)):
        if arr[read] != arr[read - 1]:
            arr[write] = arr[read]
            write += 1
    return write
```

One pointer scans (read), other maintains position for next write. O(n) time, O(1) space.

## Fast and Slow Pointers

Slow pointer moves one step, fast pointer moves two steps. Used for cycle detection and finding middle.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

If cycle exists, fast eventually catches slow. If no cycle, fast reaches end first.

Time: O(n), Space: O(1). Floyd's cycle detection algorithm.

## Finding Middle of Linked List

Use fast/slow pointers. When fast reaches end, slow is at middle.

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

Fast moves 2x speed of slow. When fast exhausts list, slow is halfway.

## Partitioning Arrays

Use two pointers to partition array based on condition (like in quicksort).

```python
def partition(arr, pivot):
    left = 0
    for right in range(len(arr)):
        if arr[right] < pivot:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
    return left
```

Left pointer marks boundary, right scans array swapping smaller elements to left side.

## Palindrome Checking

Use opposite-direction pointers to compare characters from both ends.

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

O(n) time, O(1) space. More efficient than reversing string.

## When to Use Two Pointers

Use when:
- Working with sorted arrays to find pairs/triplets
- Need to remove elements in-place
- Detecting cycles in linked lists
- Finding middle element
- Partitioning arrays
- Need O(n) alternative to nested O(n²) loops

## Benefits of Two Pointers

Reduces time complexity by avoiding nested loops.

Often achieves O(1) space by operating in-place without extra data structures.

Elegant solutions to problems that might seem to require brute force.
