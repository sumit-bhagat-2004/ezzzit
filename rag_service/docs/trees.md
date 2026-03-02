# Binary Trees and Tree Traversal

## What is a Binary Tree?

A binary tree is a hierarchical data structure where each node has at most two children: left child and right child.

The topmost node is the root. Nodes with no children are leaves. The path from root to any node defines that node's level.

## Tree Node Structure

A tree node contains data and references to left and right children:

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

Nodes are connected by parent-child relationships forming a hierarchy.

## Tree Terminology

- Root: topmost node with no parent
- Parent: node with children
- Child: node connected below another node
- Leaf: node with no children
- Height: longest path from root to leaf
- Depth: path length from root to node
- Subtree: tree formed by any node and its descendants

## Tree Traversal

Traversal means visiting all nodes in a systematic order. Different orders serve different purposes.

## Inorder Traversal

Visit left subtree, then current node, then right subtree (Left-Root-Right).

```python
def inorder(node):
    if node:
        inorder(node.left)
        process(node.val)
        inorder(node.right)
```

For binary search trees, inorder traversal visits nodes in sorted order. Time complexity: O(n).

## Preorder Traversal

Visit current node, then left subtree, then right subtree (Root-Left-Right).

```python
def preorder(node):
    if node:
        process(node.val)
        preorder(node.left)
        preorder(node.right)
```

Preorder is used to create a copy of the tree or get prefix expression. Time complexity: O(n).

## Postorder Traversal

Visit left subtree, then right subtree, then current node (Left-Right-Root).

```python
def postorder(node):
    if node:
        postorder(node.left)
        postorder(node.right)
        process(node.val)
```

Postorder is used for deleting trees or evaluating postfix expressions. Time complexity: O(n).

## Level Order Traversal (BFS)

Visit nodes level by level from left to right. Use a queue to track nodes to visit.

```python
from collections import deque
def levelorder(root):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        process(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

Time complexity: O(n), Space complexity: O(w) where w is maximum width.

## Binary Search Tree (BST)

A BST is a binary tree where for each node: all left subtree values are smaller and all right subtree values are larger.

This property enables O(log n) search in balanced BSTs. Searching compares with current node and recurses left or right.

## Tree Recursion

Tree algorithms are naturally recursive because each node's children are roots of subtrees with the same structure.

Base case is typically when node is None (empty tree). Recursive case processes node and recurses on children.

## Tree Complexity

Balanced tree operations (search, insert, delete) are O(log n) because height is logarithmic in node count.

Unbalanced trees degrade to O(n) in worst case (essentially a linked list).

Traversals visit every node once, so they're always O(n) regardless of tree shape.
