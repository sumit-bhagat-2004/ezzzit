# Strings in Python

## What are Strings?

Strings are immutable sequences of characters used for text data. Python strings support rich operations for text manipulation.

## String Creation

Create strings with single or double quotes:

```python
name = "Alice"
message = 'Hello, World!'
multiline = """This spans
multiple lines"""
```

Single and double quotes are equivalent. Triple quotes allow multiline strings.

## String Immutability

Strings cannot be modified after creation:

```python
text = "hello"
text[0] = "H"  # Error - can't modify string
text = "Hello"  # OK - creates new string
```

String operations return new strings rather than modifying originals.

## String Indexing

Access individual characters by position:

```python
word = "Python"
first = word[0]    # "P"
last = word[-1]    # "n"
```

Negative indices count from end.

## String Slicing

Extract substrings:

```python
word = "Python"
substring = word[1:4]  # "yth"
first_three = word[:3]  # "Pyt"
last_two = word[-2:]   # "on"
```

## String Concatenation

Combine strings with `+`:

```python
greeting = "Hello" + " " + "World"
repeated = "Hi" * 3  # "HiHiHi"
```

## String Methods

Strings have many built-in methods:

- `upper()`, `lower()` - change case
- `strip()` - remove whitespace from ends
- `split(delimiter)` - split into list
- `join(iterable)` - combine list items
- `replace(old, new)` - substitute text
- `find(substring)` - locate position
- `startswith()`, `endswith()` - check prefix/suffix

```python
text = "  hello world  "
clean = text.strip()  # "hello world"
words = clean.split()  # ["hello", "world"]
upper = clean.upper()  # "HELLO WORLD"
```

## String Formatting

Modern Python uses f-strings for interpolation:

```python
name = "Alice"
age = 30
message = f"My name is {name} and I'm {age} years old"
```

## String Iteration

Iterate through characters:

```python
for char in "hello":
    print(char)  # prints h, e, l, l, o
```

## Membership Testing

Check if substring exists:

```python
if "world" in "hello world":
    print("Found!")
```

## Escape Sequences

Special characters with backslash:

- `\n` - newline
- `\t` - tab
- `\\` - literal backslash
- `\"` - quote in string
