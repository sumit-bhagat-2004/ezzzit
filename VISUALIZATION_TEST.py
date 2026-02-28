# Test file demonstrating the new visualization engine

# Test 1: Array with pointers (Binary Search)
def binary_search():
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 7
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

result = binary_search()


# Test 2: Stack Operations
stack = []
stack.append(10)
stack.append(20)
stack.append(30)
stack.append(40)
top = stack[-1] if stack else None
popped = stack.pop()


# Test 3: Queue Operations (using collections.deque)
from collections import deque
queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)
front = queue.popleft()


# Test 4: Set Operations
my_set = {5, 2, 8, 1, 9}
my_set.add(3)
my_set.remove(2)


# Test 5: Dictionary/Map Operations
person_map = {"name": "Alice", "age": 25, "city": "NYC"}
person_map["country"] = "USA"


# Test 6: 2D Matrix (Dynamic Programming)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]


# Test 7: Linked List
class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
head.next.next.next = Node(4)


# Test 8: Binary Tree
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

tree = TreeNode(10)
tree.left = TreeNode(5)
tree.right = TreeNode(15)
tree.left.left = TreeNode(3)
tree.left.right = TreeNode(7)
