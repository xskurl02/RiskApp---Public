# QA / Tooling

This folder contains formatting, linting, and test configuration.

## Recommended workflow

From the repository root:

```bash
bash scripts/setup_python_env.sh
bash scripts/check_project.sh
```

`check_project.sh` runs:

```text
qa/scripts/test.sh
qa/scripts/lint.sh
python -m pip check
```

## Install QA tooling manually

If you are not using the setup script:

```bash
source .venv/bin/activate
python -m pip install -r qa/requirements-dev.txt
```

`qa/requirements-test.txt` is the smaller test-only install path. For normal development and clean validation, use `qa/requirements-dev.txt`.

## Run unit tests

```bash
bash qa/scripts/test.sh
```

Equivalent direct command:

```bash
pytest -c qa/pyproject.toml
```

## Lint

```bash
bash qa/scripts/lint.sh
```

The lint command uses Ruff with configuration from `qa/pyproject.toml`.

## Format

```bash
bash qa/scripts/format.sh
```

Use formatting intentionally; it rewrites files.

## Autofix lint issues

From the repository root:

```bash
bash scripts/check_project.sh --fix
bash scripts/check_project.sh
```

## Configuration

- `qa/pyproject.toml` configures pytest, Ruff, and Black.
- `qa/requirements-dev.txt` installs QA tools.
- The project currently does not include a pinned QA lock file.
- Server and client runtime dependencies are pinned separately in `server/requirements.lock` and `client/requirements.lock`.
