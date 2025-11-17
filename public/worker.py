# worker.py
from pyscript import sync
import ast

def check_for_multiplication(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False  # syntax errors will be caught later

    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            return True
        if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Mult):
            return True

    return False

def evaluate(code):
    code = code.replace("\t", "    ")
    namespace = {}
    try:
        exec(code, namespace)
    except Exception as e:
        return f"💥 Code failed to compile:\n{e}"

    if "multiply" not in namespace:
        return "💥 multiply function not defined"

    if check_for_multiplication(code):
        return "💥 Your solution cannot use the * operator!"

    tests = [(x, y) for x in range(-3,4) for y in range(-3,4)]

    results = []
    for test in tests:
        try:
            exec(code, namespace)
            if "multiply" not in namespace:
                results.append("error: 'multiply' function not defined")
                continue
            results.append(namespace["multiply"](test[0], test[1]))
        except Exception as e:
            results.append( f"error: {e}")
    
    formatted = ""
    correct = 0
    all_correct = False
    for test, result in zip(tests, results):
        if str(result).startswith("error:"):
            if not all_correct:
                formatted += f"💥 multiply{test} raised an exception: {result[7:]}\n"
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

