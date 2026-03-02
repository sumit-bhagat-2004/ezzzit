# Classes and Objects in Python

## What are Classes?

Classes are blueprints for creating objects. They define the structure (attributes) and behavior (methods) that objects of that class will have.

A class defines a custom data type. Objects are instances of a class, each with their own attribute values.

## Defining Classes

Use the `class` keyword followed by class name (conventionally capitalized):

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

The `__init__` method is the constructor, called when creating new objects. It initializes object attributes.

## Creating Objects

Instantiate objects by calling the class like a function:

```python
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)
```

Each object has its own copy of attributes. person1.name and person2.name are independent.

## The self Parameter

`self` refers to the current instance of the class. It must be the first parameter of instance methods.

When you call `person1.greet()`, Python automatically passes person1 as self. Inside the method, self.name accesses that object's name attribute.

## Instance Attributes vs Class Attributes

Instance attributes (defined with self) are unique per object. Each instance stores its own values.

Class attributes (defined at class level) are shared by all instances. Changing a class attribute affects all instances.

## Methods

Methods are functions defined inside a class. They operate on object data and define object behavior.

Instance methods access object attributes via self. They describe what objects can do.

```python
def greet(self):
    return f"Hello, I'm {self.name}"
```

## Object References

Variables hold references to objects, not the objects themselves. Assignment creates new references to the same object.

```python
person1 = Person("Alice", 30)
person2 = person1  # both reference same object
person2.age = 31   # changes person1.age too
```

## Memory Model

When you create an object, Python allocates memory for it. The variable stores a reference (memory address) to that object.

Object attributes are stored in the object's memory space. Accessing obj.attr looks up the attribute in that object's dictionary.

## Use Cases for Classes

Classes organize related data and functions together. They model real-world entities with attributes and behaviors.

Use classes when multiple entities share the same structure but have different values. Examples: users, products, game characters, data structures.

Classes enable encapsulation (bundling data with methods) and code reuse. They're foundational to object-oriented programming.
