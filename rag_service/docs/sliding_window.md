# Sliding Window Pattern

## What is Sliding Window?

Sliding window maintains a subset (window) of elements that slides through an array. Window expands or contracts based on conditions.

Optimizes problems that involve subarrays or substrings, reducing O(n²) or O(n³) to O(n).

## Fixed Size Window

Window size is constant. Slide window one position at a time, removing leftmost element and adding new rightmost element.

```python
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

Time: O(n) vs O(n×k) naive approach. Compute initial window once, then update incrementally.

## Variable Size Window

Window size changes dynamically. Expand window to include more elements, shrink when condition violated.

```python
def longest_substring_k_distinct(s, k):
    char_count = {}
    left = 0
    max_len = 0
    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len
```

Right pointer expands window, left pointer shrinks when invalid. Time: O(n).

## Window Management

Window boundaries defined by left and right pointers. Window size = right - left + 1.

Expand window: increment right pointer, include arr[right] in calculations.

Shrink window: increment left pointer, remove arr[left] from calculations.

## Typical Window Problems

- Maximum/minimum sum subarray of size k
- Longest substring with k distinct characters  
- Smallest subarray with sum >= target
- Find all anagrams in string
- Longest substring without repeating characters

Pattern: optimize over all subarrays meeting some condition.

## Window State Tracking

Maintain data structure (dict, set, counter) tracking window contents.

Update state when adding/removing elements. Check if current window satisfies condition.

```python
# Example: track character frequencies
char_freq = {}
char_freq[c] = char_freq.get(c, 0) + 1  # add to window
char_freq[c] -= 1  # remove from window
if char_freq[c] == 0:
    del char_freq[c]
```

## Two Pointers vs Sliding Window

Both use two pointers, but sliding window specifically maintains contiguous subarray.

Sliding window pointers move in same direction (left never goes past right). Two pointers may move in opposite directions.

Sliding window focuses on subarray optimization. Two pointers is more general technique.

## Time Complexity

Both pointers move through array at most once, each visiting every element once.

Total operations: O(2n) = O(n). Much better than O(n²) nested loops checking all subarrays.

## When to Use Sliding Window

Use when:
- Problem involves contiguous subarrays or substrings
- Need to optimize (max/min/count) over all subarrays
- Constraints define valid window (size, sum, distinct elements)
- Can update window efficiently instead of recomputing from scratch

## Sliding Window Benefits

Transforms brute force O(n²) or O(n³) into O(n) by reusing computation.

Avoids redundant recalculation by updating window incrementally.

Often achieves O(n) time with O(k) space for tracking window contents.
