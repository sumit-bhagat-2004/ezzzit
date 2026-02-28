# Python Operators

## Arithmetic Operators

Python provides standard arithmetic operators for mathematical operations on numeric values.

### Basic Arithmetic

- `+` Addition: adds two numbers
- `-` Subtraction: subtracts second from first
- `*` Multiplication: multiplies two numbers
- `/` Division: divides and returns float result
- `//` Floor Division: divides and returns integer part
- `%` Modulo: returns remainder of division
- `**` Exponentiation: raises to power

## Operator Precedence

Arithmetic operations follow mathematical precedence:
1. Parentheses ()
2. Exponentiation **
3. Multiplication, Division, Modulo (*, /, //, %)
4. Addition, Subtraction (+, -)

Example: `2 + 3 * 4` evaluates to 14, not 20.

## Expression Evaluation

Expressions are evaluated before assignment. In `result = a + b`, Python:
1. Reads values of a and b
2. Performs addition
3. Assigns result to the variable

## Augmented Assignment

Python supports compound assignment operators:

- `x += 5` equivalent to `x = x + 5`
- `x -= 3` equivalent to `x = x - 3`
- `x *= 2` equivalent to `x = x * 2`
- `x /= 4` equivalent to `x = x / 4`

These modify the variable in place with the operation result.

## Comparison Operators

Compare values and return boolean results:

- `==` Equal to
- `!=` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal
- `>=` Greater than or equal

## Logical Operators

Combine boolean expressions:

- `and` Returns True if both operands are True
- `or` Returns True if at least one operand is True
- `not` Negates the boolean value

Example: `if age >= 18 and has_license:` checks both conditions.
