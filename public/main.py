"""main.py: The main entry point pyscript.

This file registers the event listener for the "Run" button and
handles running the user's code in a worker thread with a timeout.
"""

import json

from challenge import multiply_challenge_config
from pyscript import PyWorker, document, window


def make_worker() -> PyWorker:
    """Makes a new worker thread.

    The worker uses pyodide to run Python code in a separate thread, allowing
    for a near-complete python environment.

    Returns:
        PyWorker: The worker thread.
    """
    worker = PyWorker("worker.py", type="pyodide")
    return worker


async def run(_: object) -> None:
    """Runs the user's code in a worker thread with a timeout.

    This function is attached to the "Run" button and is called when the button
    is clicked.

    Args:
        _: object: The event object (not used).
    """
    # setup
    worker = make_worker()
    config = multiply_challenge_config

    code = window.getEditorContent()  # get user implementation

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
