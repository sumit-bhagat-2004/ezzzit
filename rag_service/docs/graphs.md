# Graph Algorithms and Graph Traversal

## What is a Graph?

A graph consists of vertices (nodes) connected by edges. Graphs model relationships and connections between entities.

Can be directed (edges have direction) or undirected (edges are bidirectional). Can be weighted (edges have values) or unweighted.

## Graph Representations

Adjacency List: each vertex stores list of its neighbors. Space: O(V + E).

```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}
```

Efficient for sparse graphs. Easy to iterate over neighbors.

Adjacency Matrix: 2D array where matrix[i][j] indicates edge from vertex i to j. Space: O(V²).

Good for dense graphs or when checking edge existence quickly matters.

## Depth-First Search (DFS)

Explore as far as possible along each branch before backtracking. Use stack (or recursion) to track path.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    process(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

Time: O(V + E) - visit each vertex once, check each edge once. Space: O(V) for visited set and recursion stack.

DFS explores depth-first, going as deep as possible before backtracking. Good for detecting cycles, topological sort, maze solving.

## Breadth-First Search (BFS)

Explore all neighbors at current depth before going deeper. Use queue to track next vertices.

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        process(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

Time: O(V + E). Space: O(V) for visited set and queue.

BFS explores level by level, finding shortest path in unweighted graphs. Good for shortest path, level-order traversal.

## DFS vs BFS

DFS: uses stack/recursion, explores deep first, O(V) space for path.
- Use for: cycle detection, topological sort, path finding

BFS: uses queue, explores level by level, O(V) space for frontier.
- Use for: shortest path, nearest neighbor, level-based problems

## Cycle Detection

DFS with recursion stack tracking. If edge leads to vertex currently in stack, there's cycle.

Alternatively, track visited and recursion_stack sets. Cycle exists if visiting vertex already in recursion_stack.

## Topological Sort

Order vertices so all edges go from earlier to later vertices. Only possible in directed acyclic graphs (DAGs).

Use DFS, add vertices to stack when finishing (all descendants processed). Reverse stack gives topological order.

Applications: task scheduling, dependency resolution, build systems.

## Connected Components

Find groups of vertices where each vertex is reachable from others in group.

Run DFS/BFS from unvisited vertices. Each run finds one connected component.

Useful for network analysis, clustering, island counting problems.

## Shortest Path (Unweighted)

BFS finds shortest path in unweighted graph. Distance to each vertex is its level in BFS tree.

Track parent pointers during BFS to reconstruct path.

## Weighted Graphs

Edge weights represent distances, costs, or capacities. Shortest path requires different algorithms.

Dijkstra's algorithm: finds shortest path from source to all vertices. Uses priority queue, O(E log V).

Bellman-Ford: handles negative weights, O(VE).

A*: uses heuristic to guide search toward goal.

## Applications of Graphs

- Social networks: vertices are users, edges are friendships
- Maps: vertices are locations, edges are roads with distances
- Web: vertices are pages, directed edges are hyperlinks
- Dependencies: vertices are tasks, directed edges show prerequisites
- Communication networks: vertices are devices, edges are connections

Graphs are extremely versatile, modeling many real-world relationship problems.
