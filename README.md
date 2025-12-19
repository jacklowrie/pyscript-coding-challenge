# Pyscript Coding Challenge

This Demos how to set up a python coding challenge that runs locally in the browser (no server-side untrusted code execution). Only one challenge is provided, but the configuration is stored as a python dictionary, demonstrating how this can be adapted to support many challenges (in a database) readily.

## Live Demo
[jacklowrie.github.io/pyscript-coding-challenge/](https://jacklowrie.github.io/pyscript-coding-challenge/)

## Key files

- `srcpy/`: contains source python programs that run via pyscript
  - `main.py`: dispatches new worker threads to evaluate challenge code (any time the "run tests" button is clicked). Also, registers event hook for that button, and displays results of the run from the worker thread on the page.
  - `worker.py`: Worker thread program. Evaluates the submitted code for rules, then runs the implementation against test cases.
- `srcastro/`: contains web-related assets (content, html, etc).

