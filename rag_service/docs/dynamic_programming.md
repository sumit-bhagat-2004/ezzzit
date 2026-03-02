# Dynamic Programming Fundamentals

## What is Dynamic Programming?

Dynamic programming (DP) is an optimization technique that solves complex problems by breaking them into simpler overlapping subproblems and storing results to avoid redundant computation.

DP applies to problems with optimal substructure (optimal solution uses optimal solutions to subproblems) and overlapping subproblems (same subproblems solved multiple times).

## Memoization (Top-Down DP)

Memoization stores results of function calls in a cache. When the same inputs occur again, return cached result instead of recomputing.

```python
memo = {}
def fib(n):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```

Recursive solution with caching. Reduces fibonacci from O(2^n) to O(n).

## Tabulation (Bottom-Up DP)

Tabulation builds a table iteratively from base cases up to final answer. No recursion, pure iteration.

```python
def fib(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

Iterative solution filling table. Same O(n) time, often more efficient due to no recursion overhead.

## DP Problem Patterns

Classic DP problems include:
- Fibonacci sequence
- Longest common subsequence
- Knapsack problem
- Coin change problem
- Edit distance
- Matrix chain multiplication

Recognize DP when problem asks for optimization (min/max/count) and has overlapping subproblems.

## State Definition

DP state represents a subproblem. Define what parameters uniquely identify each subproblem.

For fibonacci, state is n (which number to compute). For knapsack, state is (items considered, remaining capacity).

## Transition Function

The recurrence relation shows how to compute state from smaller subproblems.

Fibonacci: f(n) = f(n-1) + f(n-2). Combine solutions to smaller problems to get larger solution.

## Base Cases

Base cases are smallest subproblems solved directly without recursion. They stop the recursion.

Fibonacci: f(0) = 0, f(1) = 1. Starting points for both recursive and iterative approaches.

## Space Optimization

Sometimes you can reduce space by keeping only needed previous states, not entire table.

Fibonacci only needs last two values, not all previous values. Reduce from O(n) space to O(1).

```python
def fib(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1
```

## Time Complexity

Memoized recursion: O(number of unique subproblems × time per subproblem).

For fibonacci: O(n) subproblems, O(1) each, so O(n) total.

Without DP, fibonacci is O(2^n) due to redundant recursive calls forming exponential call tree.

## When to Use DP

Use DP when:
- Problem has optimal solutions to subproblems
- Same subproblems recur multiple times
- Naive recursion is too slow
- Looking for min/max/count of ways

DP dramatically improves exponential algorithms to polynomial time by reusing computed results.
