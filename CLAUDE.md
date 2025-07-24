# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TOPL (TOML extended with placeholders) is a Python package that extends TOML files with dynamic placeholder resolution. It provides a two-phase resolution system for internal references and external parameters.

## Essential Commands

### Development Setup
```bash
# Install all dependencies including dev tools
uv sync --all-extras
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=topl --cov-report=term-missing

# Run specific test categories
uv run pytest -m unit        # Unit tests only
uv run pytest -m integration # Integration tests only
uv run pytest tests/unit/test_core.py::test_specific  # Single test
```

### Code Quality
```bash
# Linting and formatting (MUST run before committing)
uv run ruff check .
uv run ruff format .

# Type checking (MUST pass)
uv run mypy src tests

# Security scanning
uv run bandit -r src/
```

### Building and Running
```bash
# Build the package
uv build

# Run the CLI
uv run topl config.toml --external key=value

# Install locally for testing
uv pip install -e .
```

## Architecture

### Core Design: Two-Phase Resolution

The project implements a two-phase placeholder resolution system:

1. **Phase 1: Internal Resolution** - Resolves `${section.key}` references within the TOML file
   - Maximum 10 iterations to prevent infinite loops
   - Uses regex pattern matching for efficiency
   - Handles nested references automatically

2. **Phase 2: External Resolution** - Resolves `${param}` with user-supplied values
   - Single pass resolution
   - Validates all required parameters are provided
   - Returns warnings for unresolved placeholders

### Key Components

- **src/topl/core.py**: Main resolution engine (`TOPLConfig`, `resolve_placeholders`)
- **src/topl/cli.py**: Fire-based CLI interface with rich output formatting
- **src/topl/utils.py**: Helper functions for placeholder detection and resolution
- **src/topl/types.py**: Type definitions for the project

### Important Patterns

1. **TOPLConfig Wrapper**: Extends Box dictionary with metadata about resolution status
2. **Error Handling**: Custom exceptions in `exceptions.py` for domain-specific errors
3. **Configuration Constants**: Centralized in `constants.py` (e.g., MAX_INTERNAL_PASSES=10)

## Development Guidelines

### Before Committing Code

1. Ensure all tests pass: `uv run pytest`
2. Run linting and formatting: `uv run ruff check . && uv run ruff format .`
3. Verify type checking: `uv run mypy src tests`
4. Check test coverage meets 95% target

### Testing Strategy

- Write unit tests in `tests/unit/` for individual functions
- Write integration tests in `tests/integration/` for end-to-end scenarios
- Use pytest fixtures from `conftest.py` for common test data
- Test both success cases and error conditions

### Type Safety

The project uses strict mypy configuration. All public functions must have type hints.

### Version Management

Versions are automatically derived from git tags using hatch-vcs. Do not manually edit version numbers.

## Current Project Status

The project is completing Phase 1 (MVP) as tracked in WORK.md. Key features implemented:
- Two-phase placeholder resolution
- CLI interface
- Comprehensive test suite
- Full type annotations
- Package structure and tooling

Refer to TODO.md for the complete development roadmap (261 items) and WORK.md for progress tracking.