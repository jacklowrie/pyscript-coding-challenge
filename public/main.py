from pyscript import PyWorker, document

worker = PyWorker("worker.py", type="pyodide")

worker.sync.greetings = lambda: print("Pyodide bootstrapped")

print("before ready")
await worker.ready
print("after ready")

async def run(event):
    code = document.getElementById("solution").value
    result = await worker.sync.evaluate(code)
    print(result)
    document.body.append(result)

document.getElementById("run").addEventListener("click", run)
# worker.terminate()

