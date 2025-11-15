import sys
from pyscript import sync

# Use any methods from main.py on the main thread.
sync.greetings()


def evaluate(code):
    try:
        namespace = {}
        exec(code, namespace)
        return namespace["multiply"](6, 7)
    except Exception as e:
        return f"error: {e}"



# Expose any methods meant to be used from main.
sync.evaluate = evaluate
sync.heavy_computation = lambda: 6 * 7

