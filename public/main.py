# main.py
from pyscript import PyWorker, document, window
import js
import json
from challenge import multiplication_challenge as mc

def make_worker():
    worker = PyWorker("worker.py", type="pyodide")
    return worker

# ---- Initialize Ace Editor from Python ----
# Create the editor
editor = window.ace.edit(document.getElementById("solution"))
if window.matchMedia('(prefers-color-scheme: dark)').matches:
    editor.setTheme("ace/theme/monokai")
else:
    editor.setTheme("ace/theme/tomorrow")
editor.session.setMode("ace/mode/python")
editor.setOptions({
    "fontSize": "14px",
    "showPrintMargin": False,
    "tabSize": 4,
    "useSoftTabs": True,
    "wrap": True
})

editor.setValue(mc["starter_code"])
editor.clearSelection()
editor.resize()

worker = make_worker()
await worker.ready

async def run(event):
    global worker

    code = editor.getValue()
    output = document.getElementById("output")
    output.innerText = "⏳ Running..."

    # ---- TIMEOUT HANDLING ----
    timeout_ms = mc["timeout_ms"]

    # Create a promise that wraps worker.sync.evaluate
    mc_json = json.dumps(mc)
    eval_promise = worker.sync.evaluate(code, mc_json)

    # Create the timeout promise
    timeout_promise = window.Promise.new(
        lambda resolve, reject:
            window.setTimeout(lambda: reject(Exception("timeout")), timeout_ms)
    )

    try:
        # Race the worker call vs. timeout
        result = await window.Promise.race([eval_promise, timeout_promise])

        output.innerText = f"{result}"

    except Exception as e:
        if str(e) == "Error: timeout":
            # ---- Worker hung. Kill it. ----
            worker.terminate()
            worker = make_worker()   # start fresh
            await worker.ready
            output.innerText = (
                "💥 Your code took too long (possible infinite loop). Worker reset."
            )
        else:
            output.innerText = f"💥 Error: {e}"

document.getElementById("run").addEventListener("click", run)
