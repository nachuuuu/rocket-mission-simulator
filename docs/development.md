# Development Workflow

## Environment

The project targets Python 3.11 or newer and uses a `src/` package layout. The documented workstation setup is Windows with PowerShell.

Install the project and test dependency from the repository root:

```powershell
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -m pip install -e "D:\rocket-mission-simulator[dev]"
```

Run tests:

```powershell
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -m pytest
```

## Working conventions

1. Follow the milestone order in [roadmap.md](roadmap.md).
2. Keep each function focused on one physical or numerical responsibility.
3. Use SI units and include units in names when they prevent ambiguity (for example, `radius_m`).
4. Add or update tests with each behavior change.
5. Update documentation when model assumptions or public behavior changes.
6. Review the diff and run tests before committing.
7. Use descriptive commit messages that identify the milestone or change.

## Suggested Git checkpoint workflow

From PowerShell:

```powershell
git status
git diff --check
git diff
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -m pytest
git add .
git commit -m "m1: add propulsion calculations"
git push
```

Adjust the commit message to the actual change. Do not commit files unrelated to the project or unverified generated outputs.

## Repository hygiene

The project ignores the virtual environment, Python bytecode, caches, package metadata, and build outputs. Keep credentials, tokens, private data, and local machine configuration out of Git. Do not commit the `.venv/` folder.

## Tests and numerical code

Prefer deterministic unit tests for formulas and validation behavior. For numerical integration, test against analytical reference cases and record numerical settings. Use floating-point tolerances that are justified by the expected accuracy rather than demanding exact equality for approximate numerical results.
