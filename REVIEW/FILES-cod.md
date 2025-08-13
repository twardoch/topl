---
this_file: REVIEW/FILES-cod.md
---

# Repository Catalog: topl (TOML extended with placeholders)

This document catalogs the repository structure, with a filesystem tree dump and concise descriptions for every folder and file. The tree omits the internal `.git/` object store for brevity. Everything else is included.

## Filesystem Tree

```
.DS_Store
.github
.github/dependabot.yml
.github/workflows
.github/workflows/ci.yml
.github/workflows/release.yml
.github/workflows/test-pypi.yml
.gitignore
.python-version
CHANGELOG.md
CLAUDE.md
LICENSE
README.md
REPORT-2025-07-24.md
TODO.md
WORK.md
_github
_github/ISSUE_TEMPLATE
_github/ISSUE_TEMPLATE/bug_report.md
_github/ISSUE_TEMPLATE/feature_request.md
_github/PULL_REQUEST_TEMPLATE.md
_github/dependabot.yml
_github/workflows
_github/workflows/ci.yml
_github/workflows/docs.yml
_github/workflows/release.yml
docs
docs/.nojekyll
docs/github-actions-templates.md
issues
issues/101.txt
issues/102.txt
llms.txt
pyproject.toml
src
src/repo
src/repo/__init__.py
src/topl
src/topl/__init__.py
src/topl/__main__.py
src/topl/_version.py
src/topl/cli.py
src/topl/constants.py
src/topl/core.py
src/topl/exceptions.py
src/topl/py.typed
src/topl/types.py
src/topl/utils.py
src_docs
src_docs/md
src_docs/md/01-getting-started.md
src_docs/md/02-installation-setup.md
src_docs/md/03-basic-usage.md
src_docs/md/04-two-phase-resolution.md
src_docs/md/05-cli-reference.md
src_docs/md/06-api-reference.md
src_docs/md/07-configuration-examples.md
src_docs/md/08-troubleshooting.md
src_docs/md/09-development-contributing.md
src_docs/md/index.md
src_docs/mkdocs.yml
tests
tests/conftest.py
tests/integration
tests/integration/test_end_to_end.py
tests/unit
tests/unit/test_cli.py
tests/unit/test_core.py
tests/unit/test_utils.py
uv.lock
```

## Descriptions

Top-level

- .DS_Store: macOS Finder metadata; safe to remove from repo.
- .github/: canonical GitHub config (workflows, dependabot) used by GitHub.
- .gitignore: patterns for untracked files to ignore.
- .python-version: Python toolchain pin (for pyenv/uv).
- CHANGELOG.md: human-readable change history following Keep a Changelog.
- CLAUDE.md: notes related to Claude assistance or prompt; documentation only.
- LICENSE: project license (permissive SPDX file).
- README.md: project overview and user-facing intro; includes illustrative code.
- REPORT-2025-07-24.md: snapshot/report document with status notes.
- TODO.md: high-level backlog and phases; mirrors/extends WORK.md.
- WORK.md: in-repo work log; phase breakdown and current sprint status.
- _github/: alternate GitHub config folder (non-standard); duplicates some .github content.
- docs/: additional documentation (e.g., workflow templates) for manual setup.
- issues/: plain-text issue tracker items aggregated for planning.
- llms.txt: condensed repository snapshot for LLM tooling (auto-generated artifact).
- pyproject.toml: packaging, build system, and tool config; defines project metadata and dependencies.
- src/: source tree root (PEP 517 style) containing Python packages.
- src_docs/: MkDocs sources for documentation site (markdown and config).
- tests/: pytest suite with unit and integration tests.
- uv.lock: uv resolver lockfile with pinned dependencies.

.github/

- dependabot.yml: Dependabot updates for actions and Python.
- workflows/ci.yml: CI pipeline (test, lint, type check, coverage) on pushes/PRs.
- workflows/release.yml: Release pipeline (build, publish artifacts/PyPI).
- workflows/test-pypi.yml: Workflow to publish to Test PyPI for pre-releases.

_github/ (non-standard duplicate of .github)

- ISSUE_TEMPLATE/: GitHub issue templates for bug reports and feature requests.
- PULL_REQUEST_TEMPLATE.md: PR description template.
- dependabot.yml: Another Dependabot config (likely superseded by .github/dependabot.yml).
- workflows/ci.yml: CI equivalent to the canonical one.
- workflows/docs.yml: Docs build/deploy workflow (not mirrored in .github).
- workflows/release.yml: Release workflow duplicate.

docs/

- .nojekyll: disables Jekyll on GitHub Pages; required for raw assets.
- github-actions-templates.md: ready-to-copy workflow templates and instructions.

issues/

- 101.txt: planning/requirements item (feature/bug context) for development.
- 102.txt: code review notes driving quality improvements in Phase 2.

src/

- repo/: small placeholder package for repo sanity checks/examples.
  - __init__.py: trivial example entrypoint `main()` printing a greeting.
- topl/: primary package implementing TOPL.
  - __init__.py: package metadata, public exports (functions, types, exceptions).
  - __main__.py: CLI module entrypoint using Fire.
  - _version.py: auto-generated version by setuptools-scm; do not edit.
  - cli.py: CLI wiring (arg parsing, logging, file IO, error handling).
  - constants.py: regex and constants (placeholder pattern, pass limits).
  - core.py: core two-phase resolution and `TOPLConfig` wrapper.
  - exceptions.py: custom exception hierarchy for error clarity.
  - py.typed: marker enabling PEP 561 type info for the package.
  - types.py: shared typing aliases for clarity and reuse.
  - utils.py: helpers for path lookup, internal/external resolution, iterators.

src_docs/

- mkdocs.yml: MkDocs configuration for building documentation site.
- md/index.md: docs landing page.
- md/01-getting-started.md: quickstart instructions and overview.
- md/02-installation-setup.md: installation, environment setup via uv/hatch.
- md/03-basic-usage.md: simple usage examples (CLI and API).
- md/04-two-phase-resolution.md: deep dive into the resolution algorithm.
- md/05-cli-reference.md: CLI commands, options, examples.
- md/06-api-reference.md: public API documentation.
- md/07-configuration-examples.md: example TOML configurations and outputs.
- md/08-troubleshooting.md: common errors and solutions.
- md/09-development-contributing.md: contributing guidelines for developers.

tests/

- conftest.py: shared fixtures/helpers for pytest.
- integration/test_end_to_end.py: e2e tests validating CLI behavior on TOML inputs.
- unit/test_cli.py: unit tests for CLI: logging, error handling, param passing.
- unit/test_core.py: unit tests for internal/external resolution and edge cases.
- unit/test_utils.py: unit tests for helper functions and iterators.

Other notable files

- .gitignore: ignores common Python, build, and environment files.
- .python-version: sets interpreter version for local tooling consistency.
- LICENSE: license text; keep unchanged.

Notes

- Duplicate GitHub configs: both `.github/` and `_github/` exist. Standardize on `.github/` and migrate unique items (like `_github/workflows/docs.yml`) before removing `_github/`.
- README code block shows a historical inline script variant with non-ASCII quotes; real implementation lives in `src/topl/`. Consider refreshing README to mirror the packaged CLI/API.

