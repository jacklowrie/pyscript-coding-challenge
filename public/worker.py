# worker.py
import ast
import json

from pyscript import sync

op_symbol_map = {
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
symbol_op_map = {value: key for key, value in op_symbol_map.items()}


def symbol_lookup(key, by_symbol=True):
    if by_symbol:
        return symbol_op_map[key]
    else:
        return op_symbol_map[key]


def check_rules(code, config):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False  # syntax errors will be caught later

    forbidden_ops = [symbol_lookup(s) for s in config["forbidden_operators"]]
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) or isinstance(node, ast.AugAssign):
            for op in forbidden_ops:
                if isinstance(node.op, op):
                    return True, symbol_lookup(type(node.op), False)
    return False, None


def evaluate(code, config_json):
    # --- PARSE THE JSON STRING ---
    config = None
    try:
        # Parse the JSON string back into a Python dictionary
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        return f"💥 Error: Could not parse challenge data - {e}"
    except Exception as e:
        return f"💥 Unexpected error with challenge data: {e}"

    code = code.replace("\t", "    ")
    namespace = {}
    try:
        exec(code, namespace)
    except Exception as e:
        return f"💥 Code failed to compile:\n{e}"

    if config["function_name"] not in namespace:
        return f"💥 {config['function_name']} function not defined"

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
            results.append(namespace[config["function_name"]](test[0], test[1]))
        except Exception as e:
            results.append(f"error: {e}")

    formatted = ""
    correct = 0
    all_correct = False
    for test, result in zip(tests, results):
        if str(result).startswith("error:"):
            if not all_correct:
                formatted += (
                    f"💥 input {test} raised an exception: {result[7:]}\n"
                )
            all_correct = True
        elif result != test[0] * test[1]:
            if not all_correct:
                formatted += f"❌ inputs {test}. Expected {test[0] * test[1]}, got {result})\n"
            all_correct = True
        else:
            correct += 1
    output = f"{correct} / {len(tests)} correct\n" + formatted

    if correct == len(tests):
        return "✅ All tests passed! Great job!"
    else:
        return f"{correct} / {len(tests)} correct\n" + formatted


# Expose any methods meant to be used from main.
sync.evaluate = evaluate
