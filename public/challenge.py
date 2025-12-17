"""challenges.py: challenge configurations for code exercises.

This file contains all the details for the challenge. In a real
application, this can be stored in a database or CMS.
"""

multiply_challenge_config = {
    "function_name": "multiply",
    "forbidden_operators": ["*"],
    "test_cases": [(x, y) for x in range(-10, 11) for y in range(-10, 11)],
    "timeout_ms": 3000,
}
