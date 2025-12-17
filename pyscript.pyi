from typing import Any

# Minimal stub for pyscript used in the browser/pyodide environment
class PyWorker:
    def __init__(
        self,
        path: str,
        /,
        *args: object,
        **kwargs: object,
    ) -> None: ...

    # Awaitable that resolves when the worker is ready
    ready: Any

    # Object exposing bridged calls (used like
    # `worker.sync.evaluate(...)`)
    sync: Any

    def terminate(self) -> None: ...

sync: Any
document: Any
window: Any
