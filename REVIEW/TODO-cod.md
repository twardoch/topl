---
this_file: REVIEW/TODO-cod.md
---

# Improvement Plan (Proposals + Examples)

This is a concrete, example-backed plan to improve this repository without changing product scope. It prioritizes small, safe, high-impact steps that align with current structure and tests.

## Priorities at a Glance

- Repo hygiene: unify GitHub configs; remove duplication
- Logging: add optional structured logging with loguru (keep stdlib default)
- CLI UX: dry-run, validate, exit codes, better help, shell completion
- Docs: publish MkDocs to GitHub Pages; update README to reflect package
- Performance: simple benchmarks and big-file smoke tests
- CI: CodeQL, docs deploy, coverage gates, pinned toolchain
- Packaging: tidy metadata; ensure reproducible builds

## 1) Repo Hygiene and Consistency

- Consolidate GitHub config
  - Move unique items from `_github/` into `.github/` (notably `_github/workflows/docs.yml`). Remove `_github/` afterwards to avoid confusion.
  - Ensure only one Dependabot file remains in `.github/`.
- Clarify README
  - Replace the old inline “script-style” example with accurate, small examples using `topl` package API/CLI.
  - Mention two-phase algorithm briefly; link to docs for details.

Example README snippet:

```md
Quick start

```toml
# config.toml
name = "world"
greeting = "Hello {{name}}!"
```

```bash
topl config.toml
{"name": "world", "greeting": "Hello world!"}
```
```

## 2) Logging: optional loguru adapter

Goal: keep current stdlib logging as default; optionally enable loguru for richer local debugging without breaking library users.

Steps

- Add a tiny adapter that wires stdlib logs into loguru if `TOPL_USE_LOGURU=1` or CLI `--loguru` is passed.
- Keep `logging` calls in code as-is to avoid invasive changes.

Example adapter:

```python
# src/topl/logging_ext.py
from __future__ import annotations
import logging, os
from typing import Any

_ENABLED = os.getenv("TOPL_USE_LOGURU") == "1"

def maybe_enable_loguru(verbose: bool) -> None:
    if not _ENABLED:
        return
    try:
        from loguru import logger as _logger
    except Exception:
        return
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            level = _logger.level(record.levelname).name if record.levelname in _logger._levels else record.levelno
            _logger.log(level, record.getMessage())
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.DEBUG if verbose else logging.INFO)
```

CLI hook:

```python
from .logging_ext import maybe_enable_loguru

def main_cli(path: str, verbose: bool = False, use_loguru: bool = False, **params: str) -> None:
    configure_logging(verbose)
    if use_loguru:
        maybe_enable_loguru(verbose)
    # ...
```

## 3) CLI UX enhancements

- Add `--dry-run`: parse + resolve, but return non-zero if unresolved placeholders remain; print a diff-like preview.
- Add `--validate`: only parse TOML and run internal checks; no output mutation.
- Exit codes: 0 success; 1 invalid input; 2 unresolved placeholders; 3 circular reference.
- Shell completion: generate via Fire or click-completion shim; document install steps.

Example behavior:

```bash
topl config.toml --dry-run
# prints resolution plan and exits 0 if everything resolves, 2 otherwise

topl config.toml --validate
# validates TOML only; exits 0 on valid, 1 on parse error
```

## 4) Performance and scale checks

- Add `benchmarks/` with `pytest-benchmark` scenarios:
  - Many small placeholders
  - Large nested objects
  - Mixed internal/external placeholders
- Add big-file smoke test in `tests/perf/` guarded by `-m slow` marker.

Example benchmark:

```python
def test_resolve_many_placeholders(benchmark):
    data = {f"k{i}": f"v{{{{k{i-1}}}}}" for i in range(1, 2000)}
    data["k0"] = "root"
    import tomllib, topl
    bm = benchmark(lambda: topl.resolve_placeholders(data))
```

## 5) Documentation flow

- Publish MkDocs
  - Reuse existing `src_docs/mkdocs.yml` and `src_docs/md`. Add a simple GH Action deploying to GitHub Pages.
  - Update README badges: docs, CI, PyPI.

Docs workflow (example):

```yaml
# .github/workflows/docs.yml
name: Docs
on:
  push:
    branches: [ main ]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install mkdocs-material mkdocs
      - run: mkdocs gh-deploy --force --config-file src_docs/mkdocs.yml
```

## 6) CI/CD hardening

- Add CodeQL security scanning workflow.
- Upload coverage thresholds; fail if coverage < 90% (configurable).
- Cache uv and pip wheels in CI for speed; pin action versions.
- Add `pre-commit` config and a CI job to run it.

Coverage gate example:

```yaml
- name: Run tests with coverage
  run: |
    uv run pytest --cov=topl --cov-report=term-missing --cov-fail-under=90
```

## 7) Packaging polish

- Ensure `pyproject.toml` includes project URLs, classifiers, readme content type.
- Verify `py.typed` is included in the built wheel (already present).
- Add `python_requires >= 3.11` if that’s the target baseline.
- Add SDist and wheel reproducibility check in CI.

Example `pyproject.toml` additions:

```toml
[project.urls]
Homepage = "https://github.com/OWNER/topl"
Documentation = "https://OWNER.github.io/topl/"
Issues = "https://github.com/OWNER/topl/issues"
Changelog = "https://github.com/OWNER/topl/blob/main/CHANGELOG.md"
```

## 8) API quality and safety

- Input validation: enforce string-only substitution targets; clear errors on non-string leaves.
- Safer external params: reject keys containing spaces or braces; document accepted formats.
- Structured errors: include key path in exceptions where applicable.

Example guard in `resolve_external`:

```python
for k in params:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_\.]*", k):
        raise InvalidTOMLError(f"Invalid external key: {k}")
```

## 9) Developer experience

- Makefile or `uvx` tasks for common commands (lint, test, type, format).
- Add `nox` sessions for multi-Python matrix locally.
- Document “one-liner” dev setup in README.

Example Makefile targets:

```make
lint: ; uv run ruff check .
fmt: ; uv run ruff format . && uv run ruff check --fix .
type: ; uv run mypy src tests
test: ; uv run pytest -q
all: fmt lint type test
```

## 10) Security and compliance

- Add `SECURITY.md` with vulnerability disclosure process.
- Add SBOM generation (e.g., `pip-licenses` or `cyclonedx-bom`).
- Path traversal protection in CLI: refuse paths outside CWD unless `--allow-outside` passed.

Example SBOM step (CI):

```yaml
- name: Generate SBOM
  run: uvx cyclonedx-bom -o sbom.json
```

---

## Roadmap (phased)

- Phase A (Hygiene, 1–2 hours)
  - Unify `.github/` and `_github/`; migrate docs workflow; remove duplicates
  - Refresh README quickstart; add badges placeholders

- Phase B (Docs + CI, 2–4 hours)
  - Add docs deploy workflow; publish to Pages
  - Add coverage gate; pin actions; enable CodeQL

- Phase C (CLI + Logging, 3–5 hours)
  - Implement `--dry-run` and `--validate`; exit codes
  - Add optional loguru adapter

- Phase D (Perf + DX, 3–5 hours)
  - Add benchmarks and slow tests
  - Add Makefile/nox; pre-commit config

## Acceptance criteria

- Single source of truth under `.github/`; workflows green across platforms
- README mirrors package reality; docs can be browsed via GitHub Pages
- CLI exposes `--dry-run` and `--validate` with deterministic exit codes
- Optional loguru integration works without impacting library consumers
- Coverage threshold enforced; SBOM produced on CI

## Risks and mitigations

- Fire CLI flags collision: prefer keyword-only additions; document clearly
- Docs deploy permissions: use Pages with standard permissions; test via PRs
- Loguru optionality: default off, env/flag to enable; do not import at module top-level

## Out-of-scope (for now)

- Async I/O layer and plugin architecture (mentioned in TODO.md) — keep in backlog
- Streaming mode — requires API refactor; evaluate post-1.0 hardening

