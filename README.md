# Pyscript Coding Challenge

This Demos how to set up a python coding challenge that runs locally in the browser (no server-side untrusted code execution). Only one challenge is provided, but the configuration is stored as a python dictionary, demonstrating how this can be adapted to support many challenges (in a database) readily.

## Key files

- `srcastro`: contains web-related assets.
- `srcpy`: contains source python programs that run via pyscript
  - `main.py`: dispatches new worker threads to evaluate challenge code (any time the "run tests" button is clicked)
  - `worker.py`: Worker thread program. Evaluates the submitted code for rules, then runs the implementation against test cases.
