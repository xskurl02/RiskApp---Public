# QA / Tooling

This folder contains formatting, linting, and test config.

## Install (dev/test)

From the repository root:

```bash
python -m pip install -r qa/requirements-test.txt
```

## Run unit tests

```bash
pytest -c qa/pyproject.toml
```

You can also use the convenience script:

```bash
bash qa/scripts/test.sh
```

## Lint / Format

```bash
# lint
bash qa/scripts/lint.sh

# format
bash qa/scripts/format.sh
```

> Config lives in `qa/pyproject.toml`; the scripts pass `--config qa/pyproject.toml`.
