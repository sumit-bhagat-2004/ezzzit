# Sorting Algorithms

## What is Sorting?

Sorting arranges elements in a specific order (ascending or descending). It's fundamental to many algorithms and enables efficient searching.

Sorting complexity matters for large datasets. Different algorithms have different time/space tradeoffs.

## Bubble Sort

Compare adjacent elements and swap if out of order. Repeat until no swaps needed.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

Time complexity: O(n²) average and worst case, O(n) best case (already sorted). Space: O(1).

Simple but inefficient for large datasets. Largest elements "bubble" to the end each pass.

## Selection Sort

Find minimum element and swap it to front. Repeat for remaining unsorted portion.

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

Time complexity: O(n²) all cases. Space: O(1). 

Makes fewest swaps, useful when swap operations are expensive.

## Insertion Sort

Build sorted array one element at a time by inserting each element into its correct position.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

Time complexity: O(n²) average/worst, O(n) best (already sorted). Space: O(1).

Efficient for small or nearly sorted arrays. Used in hybrid algorithms like Timsort.

## Merge Sort

Divide array in half recursively, sort each half, then merge sorted halves.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

Time complexity: O(n log n) all cases. Space: O(n) for merge array.

Stable sort (preserves relative order of equal elements). Good for linked lists.

## Quick Sort

Choose pivot, partition array so smaller elements are left of pivot and larger are right. Recursively sort partitions.

```python
def quick_sort(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
```

Time complexity: O(n log n) average, O(n²) worst case. Space: O(log n) for recursion stack.

Fast in practice with good pivot selection. Unstable. Used as default in many libraries.

## Comparison of Sorting Algorithms

Simple O(n²) sorts (bubble, selection, insertion):
- Good for small arrays (< 50 elements)
- Low overhead, in-place
- Insertion sort good for nearly sorted data

Efficient O(n log n) sorts (merge, quick):
- Required for large datasets
- Merge sort: stable, O(n) space, predictable performance
- Quick sort: fast average case, in-place, but O(n²) worst case

## Stability in Sorting

A stable sort preserves the relative order of equal elements. If two elements compare equal, they appear in same order in output as input.

Stable: merge sort, insertion sort. Unstable: quick sort, heap sort.

Stability matters when sorting by multiple keys or when equal elements have associated data.

## In-Place vs Out-of-Place

In-place sorts use O(1) extra space (ignoring recursion stack): bubble, selection, insertion, quick sort.

Out-of-place sorts need O(n) additional space: merge sort creates new arrays during merging.

In-place saves memory but may be harder to implement correctly.

## Choosing a Sorting Algorithm

For general use: Python's built-in sorted() or list.sort() (Timsort, O(n log n), stable).

For small arrays or nearly sorted: insertion sort.

For guaranteed O(n log n): merge sort.

For average case speed and in-place: quick sort with median-of-three pivot.

Consider: data size, memory constraints, stability requirements, data characteristics.
