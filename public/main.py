# main.py
from pyscript import PyWorker, document, window
import js

# ---- Initialize Ace Editor from Python ----
# Create the editor
editor = window.ace.edit(document.getElementById("solution"))
editor.setTheme("ace/theme/tomorrow")
editor.session.setMode("ace/mode/python")
editor.setOptions({
    "fontSize": "14px",
    "showPrintMargin": False,
    "tabSize": 4,
    "useSoftTabs": True,
    "wrap": True
})

editor.setValue("# your imports here\n\ndef multiply(a, b):\n    # your code here ")
editor.resize()

worker = PyWorker("worker.py", type="pyodide")
await worker.ready

async def run(event):
    global worker

    code = editor.getValue()
    document.getElementById("output").innerText = "⏳ Running..."

    # ---- TIMEOUT HANDLING ----
    timeout_ms = 1500  # 1.5 second limit

    # Create a promise that wraps worker.sync.evaluate
    eval_promise = worker.sync.evaluate(code)

    # Create the timeout promise
    timeout_promise = window.Promise.new(
        lambda resolve, reject:
            window.setTimeout(lambda: reject(Exception("timeout")), timeout_ms)
    )

    try:
        # Race the worker call vs. timeout
        result = await window.Promise.race([eval_promise, timeout_promise])

        document.getElementById("output").innerText = f"{result}"

    except Exception as e:
        if str(e) == "Error: timeout":
            # ---- Worker hung. Kill it. ----
            worker.terminate()
            worker = make_worker()   # start fresh
            await worker.ready
            document.getElementById("output").innerText = (
                "💥 Your code took too long (possible infinite loop). Worker reset."
            )
        else:
            document.getElementById("output").innerText = f"💥 Error: {e}"

document.getElementById("run").addEventListener("click", run)

