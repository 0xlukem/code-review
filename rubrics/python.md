# Python rubric overlay

Apply in addition to the base rubric when the PR touches Python code.

## P0/P1 candidates

- Mutable default arguments (`def f(x=[])`)
- Bare or broad `except:` swallowing errors
- SQL or shell commands built with string formatting (injection)
- Unclosed resources (files, connections) — prefer context managers
- Mutable class attributes shared across instances

## P2 candidates

- Missing type hints on new public functions
- Blocking I/O inside async code
- `datetime.now()` without timezone where it matters
- Growing global state or module-level mutable singletons

## P3 candidates

- Naming and import order beyond what ruff/black already enforce — skip entirely if the repo has them configured
