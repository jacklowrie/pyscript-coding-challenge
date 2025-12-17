# main.py
from pyscript import PyWorker, document, window
import json
from pyscript.ffi import is_none
from challenge import multiply_challenge_config


def make_worker():
    worker = PyWorker("worker.py", type="pyodide")
    return worker


async def run(event):
    # setup
    worker = make_worker()
    config = multiply_challenge_config
    editor = window.editor

    code = editor.getValue()  # get user implementation

    # update output to indicate tests are running
    output = document.getElementById("output")
    output.innerText = "⏳ Running..."

    # Create a promise that wraps worker.sync.evaluate
    await worker.ready
    eval_promise = worker.sync.evaluate(code, json.dumps(config))

    # Create the timeout promise
    timeout_promise = window.Promise.new(
        lambda resolve, reject: window.setTimeout(
            lambda: reject(Exception("timeout")), config["timeout_ms"]
        )
    )

    try:
        # Race the worker call against the timeout.
        result = await window.Promise.race([eval_promise, timeout_promise])

        # display results and exit
        output.innerText = f"{result}"
        worker.terminate()

    except Exception as e:
        if str(e) == "timeout":
            # ---- Worker hung. Kill it. ----
            worker.terminate()
            output.innerText = (
                "💥 Your code took too long (possible infinite loop)."
            )
        else:
            output.innerText = f"💥 Error: {e}"


# ---- Attach event listener to run button ----
document.getElementById("run-btn").addEventListener("click", run)
