# worker.py
from pyscript import sync

def evaluate(code):
    code = code.replace("\t", "    ")
    print(code)
    namespace = {}
    try:
        exec(code, namespace)
    except Exception as e:
        return f"💥 Code failed to compile:\n{e}"

    if "multiply" not in namespace:
        return "💥 multiply function not defined"

    tests = [
        (1,1),
        (1,2),
        (2,1),
        (2,3),
        (0,3),
        (3,0),
        (-2,3),
        (2,-3),
    ]
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
    for test, result in zip(tests, results):
        if str(result).startswith("error:"):
            formatted += f"💥 multiply{test} raised an exception: {result[7:]}\n"
        elif result == test[0] * test[1]:
            formatted += f"✅ multiply{test} = {result} (correct)\n"
        else:
            formatted += f"❌ multiply{test} = {result} (incorrect, expected {test[0] * test[1]})\n"

    return formatted






# Expose any methods meant to be used from main.
sync.evaluate = evaluate

