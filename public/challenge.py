""" challenges.py: challenge configurations for code exercises.

This file contains all the details for the challenge. In a real (prod)
application, this can be stored in a database or CMS.
 """

multiplication_challenge = {
    "function_name": "multiply",
    "title": "Implement Multiplication Without Using '*' Operator",
    "description": (
        "Define a function `multiply(a, b)` that returns the product of `a` and `b` "
        "without using the `*` operator. You can use addition, subtraction, and loops."
    ),
    "starter_code": (
        "# your imports here\n\n"
        "def multiply(a, b):\n"
        "    # your code here"
    ),
    "forbidden_operators": ["*"],
    "test_cases": [
        (x, y) for x in range(-3, 4) for y in range(-3, 4)
    ],
    "timeout_ms": 1500,
}