# Complete Test Suite for All Data Structure Visualizations

print("=== Testing Stack, Queue, Set, Map Visualizations ===\n")

# Test 1: Stack (Vertical "Jar" visualization)
print("1. Stack Operations:")
stack = []
stack.append(10)
stack.append(20)
stack.append(30)
stack.append(40)
stack.append(50)
print(f"Stack after pushes: {stack}")

top_element = stack[-1]
print(f"Top element: {top_element}")

popped = stack.pop()
print(f"Popped: {popped}")
print(f"Stack after pop: {stack}\n")


# Test 2: Queue (Horizontal "Pipe" visualization)
print("2. Queue Operations using deque:")
from collections import deque
queue = deque()
queue.append(100)  # Enqueue
queue.append(200)
queue.append(300)
queue.append(400)
print(f"Queue after enqueues: {list(queue)}")

first = queue.popleft()  # Dequeue
print(f"Dequeued: {first}")
print(f"Queue after dequeue: {list(queue)}\n")


# Test 3: Set (Floating "Cloud" visualization)
print("3. Set Operations:")
my_set = {5, 2, 8, 1, 9}
print(f"Initial set: {my_set}")

my_set.add(3)
print(f"After adding 3: {my_set}")

my_set.add(7)
print(f"After adding 7: {my_set}")

my_set.remove(2)
print(f"After removing 2: {my_set}\n")


# Test 4: Dictionary/Map (Key-Value pairs with arrows)
print("4. Dictionary/Map Operations:")
person_map = {"name": "Alice", "age": 25}
print(f"Initial map: {person_map}")

person_map["city"] = "NYC"
person_map["country"] = "USA"
print(f"After additions: {person_map}")

person_map["age"] = 26
print(f"After updating age: {person_map}\n")


# Test 5: Array with pointers (for comparison)
print("5. Array with Binary Search pointers:")
arr = [1, 3, 5, 7, 9, 11, 13, 15]
target = 7
low = 0
high = len(arr) - 1

while low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        print(f"Found {target} at index {mid}")
        break
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1

print("\n=== All Tests Complete ===")
