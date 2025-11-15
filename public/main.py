# main.py
from pyscript import PyWorker, document, window

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

editor.setValue("def multiply(a, b):\n    # your code here ")
editor.resize()

worker = PyWorker("worker.py", type="pyodide")
await worker.ready

async def run(event):
    code = editor.getValue()
    result = await worker.sync.evaluate(code)
    document.getElementById("output").innerText = f"Results:\n {result}"

document.getElementById("run").addEventListener("click", run)

