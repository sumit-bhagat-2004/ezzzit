# Conditional Branching in Python

## What are Conditionals?

Conditionals allow programs to make decisions and execute different code paths based on boolean conditions. They enable control flow that responds to runtime values.

## If Statements

The `if` statement executes code only when a condition is True:

```python
if temperature > 30:
    print("It's hot")
```

The condition is evaluated first. If True, the indented block executes. If False, it's skipped.

## If-Else Statements

The `else` clause provides an alternative path when the condition is False:

```python
if score >= 60:
    print("Pass")
else:
    print("Fail")
```

Exactly one branch executes - either the if block or the else block.

## Elif for Multiple Conditions

Use `elif` (else if) to check multiple conditions in sequence:

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

Python checks conditions from top to bottom. The first True condition executes its block, then skips remaining branches.

## Boolean Conditions

Conditions are expressions that evaluate to True or False. Common patterns:

- Comparisons: `x > 5`, `name == "Alice"`
- Logical combinations: `age >= 18 and has_license`
- Truthiness: empty lists/strings are False, non-empty are True

## Nested Conditionals

Conditionals can be nested inside other conditionals:

```python
if logged_in:
    if is_admin:
        show_admin_panel()
    else:
        show_user_dashboard()
```

Each level checks a different condition. Indentation shows the nesting structure.

## Conditional Expressions

Python supports inline conditional expressions (ternary operator):

```python
result = "even" if x % 2 == 0 else "odd"
```

This assigns one of two values based on a condition.
