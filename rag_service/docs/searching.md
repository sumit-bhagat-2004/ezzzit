# Searching Algorithms

## What is Searching?

Searching finds the position or existence of a target value in a collection. Efficiency depends on data structure and whether data is sorted.

## Linear Search

Check each element sequentially until finding target or reaching end.

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

Time complexity: O(n) - must check every element in worst case. Space: O(1).

Works on unsorted data. Only option for unsorted arrays or linked lists.

## Binary Search

For sorted arrays, repeatedly divide search space in half by comparing target with middle element.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Time complexity: O(log n). Space: O(1) iterative, O(log n) recursive.

Requires sorted array. Much faster than linear search for large datasets.

## Binary Search Logic

Each comparison eliminates half the remaining elements. With n elements, at most log₂(n) comparisons needed.

Moving left pointer up searches right half. Moving right pointer down searches left half.

Loop terminates when left > right (element not found) or arr[mid] == target (found).

## Recursive Binary Search

Binary search can be implemented recursively by passing narrowed range:

```python
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

Same O(log n) time, but O(log n) space for call stack.

## Binary Search Variations

Find first occurrence: when finding target, continue searching left to find earliest position.

Find last occurrence: when finding target, continue searching right to find latest position.

Find insertion point: when element not found, left pointer marks where to insert to maintain sorted order.

## Search Space Reduction

Binary search exemplifies divide and conquer. Problem size halves each iteration.

This logarithmic growth makes binary search scale well. Searching 1 million elements needs only ~20 comparisons.

## Binary Search Requirements

Array must be sorted. Binary search on unsorted data gives incorrect results.

If sorting cost O(n log n) is amortized over many searches, binary search becomes worthwhile. Single search may be faster with linear search.

## Hash Table Search

Hash tables provide O(1) average case search by computing index from key value.

Trade space for time: use extra memory for hash table to get constant time lookups.

Python dictionaries and sets use hash tables internally.

## Comparison: Linear vs Binary

Linear search: O(n), works on any data, simple to implement.

Binary search: O(log n), requires sorted data, more complex but much faster for large n.

For small arrays (n < 10), linear search may be faster due to lower constant factors.

## Search Algorithm Selection

Unsorted data: linear search (only option).

Sorted array, single search: binary search if n is large, otherwise linear.

Sorted array, many searches: binary search.

Need O(1) lookup and have memory: hash table.

Consider: data size, sort status, number of searches, memory constraints.
