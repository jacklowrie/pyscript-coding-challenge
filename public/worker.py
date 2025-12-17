"""worker.py: The worker thread for evaluating user code.

The worker thread evaluates the user's code agains the challenge
rules, then executes the code against the test cases. It sends
the formated results back to the main thread (`main.py`), which
displays them to the user.
"""

import ast
import json
from typing import Any, overload

from pyscript import sync

op_symbol_map: dict[type, str] = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.FloorDiv: "//",
    ast.Mod: "%",
    ast.Pow: "**",
    ast.BitAnd: "&",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
}
symbol_op_map: dict[str, type] = {
    value: key for key, value in op_symbol_map.items()
}


@overload
def _convert_op(key: str) -> type[ast.operator]: ...  # ← just a type hint


@overload
def _convert_op(key: type[ast.operator]) -> str: ...  # ← just a type hint


def _convert_op(key: str | type) -> type | str:
    """Converts between operator symbols and AST operator types.

    Args:
        key: The AST operator or symbol to convert.

    Returns:
        The converted operator.
    """
    if isinstance(key, str):
        return symbol_op_map[key]
    else:
        return op_symbol_map[key]


def check_rules(code: str, config: dict) -> tuple[bool, str | None]:
    """Checks the user's code for rule violations.

    Args:
        code: The user's code as a string.
        config: The challenge configuration dictionary.

    Returns:
        A 2-value tuple where the first element indicates if a rule was
        violated, and the second element is the symbol of the violated operator
        (if any).
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False, None  # syntax errors will be caught later

    forbidden_ops = [_convert_op(s) for s in config["forbidden_operators"]]
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) or isinstance(node, ast.AugAssign):
            for op in forbidden_ops:
                if isinstance(node.op, op):
                    return True, _convert_op(type(node.op))
    return False, None


def evaluate(code: str, config_json: str) -> str:
    """Evaluates the user's code against the challenge configuration.

    Args:
        code: The user's code as a string.
        config_json: The challenge configuration as a JSON string.

    Returns:
        The formatted results of the evaluation.
    """
    config = None
    try:
        # Parse the JSON string back into a Python dictionary
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        return f"💥 Error: Could not parse challenge data - {e}"
    except Exception as e:
        return f"💥 Unexpected error with challenge data: {e}"

    code = code.replace("\t", "    ")
    namespace: dict[str, Any] | None = {}
    try:
        exec(code, namespace)
    except Exception as e:
        return f"💥 Code failed to compile:\n{e}"

    if namespace is None or config["function_name"] not in namespace.keys():
        return f"💥 {config['function_name']} function not defined"

    func = namespace.get(config["function_name"])
    if not callable(func):
        return f"💥 {config['function_name']} is not a function"

    rule_violation, symbol = check_rules(code, config)
    if rule_violation:
        return f"💥 Your solution cannot use the {symbol} operator!"

    tests = config["test_cases"]

    results = []
    for test in tests:
        try:
            exec(code, namespace)
            if config["function_name"] not in namespace:
                results.append(
                    f"error: '{config['function_name']}' function not defined"
                )
                continue
            results.append(func(test[0], test[1]))
        except Exception as e:
            results.append(f"error: {e}")

    formatted = ""
    correct = 0
    all_correct = False
    for test, result in zip(tests, results, strict=True):
        if str(result).startswith("error:"):
            if not all_correct:
                formatted += (
                    f"💥 input {test} raised an exception: {result[7:]}\n"
                )
            all_correct = True
        elif result != test[0] * test[1]:
            if not all_correct:
                formatted += (
                    f"❌ inputs {test}. Expected {test[0] * test[1]}, "
                    f"got {result})\n"
                )
            all_correct = True
        else:
            correct += 1
    score = f"{correct} / {len(tests)} correct\n"

    if correct == len(tests):
        return score + "✅ All tests passed! Great job!"
    else:
        return score + formatted


# Expose any methods meant to be used from main.
sync.evaluate = evaluate
