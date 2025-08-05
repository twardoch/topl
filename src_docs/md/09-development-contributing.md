# Chapter 9: Development & Contributing

Guide for developers who want to contribute to TOPL, extend its functionality, or set up a development environment.

## Development Setup

### Prerequisites

- **Python 3.11+** (required for modern type hints)
- **uv** (recommended) or **pip** for package management
- **Git** for version control
- **Make** (optional, for convenience commands)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/terragonlabs/topl.git
cd topl

# Install with all development dependencies
uv sync --all-extras

# Or with pip
pip install -e ".[dev,docs,test]"

# Verify installation
python -m pytest
python -m mypy src tests
```

### Development Environment

#### Using uv (Recommended)

```bash
# Create virtual environment with correct Python version
uv venv --python 3.11

# Install all dependencies including optional ones
uv sync --all-extras

# Activate environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install pre-commit hooks
pre-commit install
```

#### Using pip + virtualenv

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev,docs,test]"

# Install pre-commit hooks
pre-commit install
```

## Project Structure

```
topl/
├── src/
│   └── topl/
│       ├── __init__.py          # Public API exports
│       ├── __main__.py          # CLI entry point  
│       ├── cli.py               # Command-line interface
│       ├── core.py              # Main resolution logic
│       ├── utils.py             # Helper functions
│       ├── exceptions.py        # Custom exceptions
│       ├── types.py             # Type definitions
│       ├── constants.py         # Configuration constants
│       └── py.typed             # Type information marker
├── tests/
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── conftest.py              # Pytest configuration
├── docs/                        # Documentation output
├── src_docs/                    # Documentation sources
├── pyproject.toml               # Project configuration
├── README.md                    # Project overview
├── CHANGELOG.md                 # Release notes
└── CLAUDE.md                    # Development instructions
```

### Key Components

#### Core Module (`src/topl/core.py`)
- `resolve_placeholders()` - Main resolution function
- `TOPLConfig` - Wrapper class for resolved configuration
- Two-phase resolution logic

#### CLI Module (`src/topl/cli.py`)  
- `main_cli()` - CLI entry point
- `load_toml_file()` - File loading with error handling
- Rich console output formatting

#### Utils Module (`src/topl/utils.py`)
- `get_by_path()` - Dotted path value retrieval
- `resolve_internal_once()` - Single internal resolution pass
- `resolve_external()` - External parameter resolution
- `iter_box_strings()` - String value iteration

## Development Workflow

### 1. Code Style and Quality

TOPL follows strict code quality standards:

```bash
# Run all quality checks
uv run ruff check .                    # Linting
uv run ruff format .                   # Formatting  
uv run mypy src tests                  # Type checking
uv run bandit -r src/                  # Security scanning
```

#### Automated with Pre-commit

```bash
# Install pre-commit hooks (one-time setup)
pre-commit install

# Hooks run automatically on commit
git commit -m "Your changes"

# Run manually on all files
pre-commit run --all-files
```

### 2. Testing

#### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=topl --cov-report=term-missing

# Run specific test categories
uv run pytest -m unit                 # Unit tests only
uv run pytest -m integration          # Integration tests only

# Run specific test file
uv run pytest tests/unit/test_core.py

# Run with verbose output
uv run pytest -v
```

#### Writing Tests

##### Unit Tests
```python
# tests/unit/test_new_feature.py
import pytest
from topl.core import resolve_placeholders


def test_new_feature():
    """Test description of what the feature does."""
    data = {"test": {"value": "${param}"}}
    config = resolve_placeholders(data, param="expected")
    
    assert config.test.value == "expected"
    assert not config.has_unresolved


def test_new_feature_error_case():
    """Test error handling in new feature."""
    with pytest.raises(ValueError, match="expected error message"):
        # Code that should raise ValueError
        pass
```

##### Integration Tests
```python
# tests/integration/test_end_to_end_new_feature.py
import tempfile
from pathlib import Path
from topl.cli import main_cli


def test_cli_new_feature():
    """Test new feature through CLI interface."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write('value = "${TEST_PARAM}"\n')
        f.flush()
        
        # Test CLI with new feature
        main_cli(f.name, TEST_PARAM="success")
        
    Path(f.name).unlink()  # Cleanup
```

#### Test Coverage

Maintain 95%+ test coverage:

```bash
# Generate coverage report
uv run pytest --cov=topl --cov-report=html

# View in browser
open htmlcov/index.html
```

### 3. Documentation

#### Building Documentation

```bash
# Install documentation dependencies
uv sync --extra docs

# Build documentation
cd src_docs
mkdocs serve

# Build for production
mkdocs build
```

#### Writing Documentation

- Use clear, concise examples
- Include both success and error cases
- Test all code examples
- Update relevant chapters when adding features

### 4. Version Management

TOPL uses `hatch-vcs` for automatic version management:

```bash
# Version is automatically derived from git tags
git tag v1.2.3
git push origin v1.2.3

# Check current version
python -c "from topl import __version__; print(__version__)"
```

## Contributing Guidelines

### 1. Issues and Feature Requests

Before contributing:

1. **Search existing issues** on [GitHub](https://github.com/terragonlabs/topl/issues)
2. **Create detailed issue** with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information
   - Minimal example

### 2. Pull Request Process

#### Before Starting

1. **Fork the repository** on GitHub
2. **Create feature branch** from `main`:
   ```bash
   git checkout -b feature/new-functionality
   ```
3. **Discuss major changes** in an issue first

#### Development Process

1. **Write tests first** (TDD approach preferred)
2. **Implement feature** with proper error handling
3. **Add documentation** including examples
4. **Update CHANGELOG.md** with your changes
5. **Ensure all checks pass**:
   ```bash
   uv run pytest
   uv run mypy src tests
   uv run ruff check .
   ```

#### Submitting PR

1. **Push to your fork**:
   ```bash
   git push origin feature/new-functionality
   ```
2. **Create Pull Request** with:
   - Clear title and description
   - Link to related issues
   - Screenshots/examples if applicable
   - Checklist completion

#### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Added/updated tests
- [ ] Added/updated documentation
- [ ] Updated CHANGELOG.md
```

### 3. Code Standards

#### Python Style

Follow PEP 8 and project conventions:

```python
# Good: Clear, descriptive names
def resolve_placeholders(data: ConfigMapping, **params: str) -> TOPLConfig:
    """Resolve placeholders in configuration data.
    
    Args:
        data: Configuration data from TOML file
        **params: External parameters for resolution
        
    Returns:
        Resolved configuration with metadata
        
    Raises:
        CircularReferenceError: If circular references detected
    """
    # Implementation with clear variable names
    config = Box(data, default_box=True)
    
    # Use descriptive loop variables
    for pass_number in range(MAX_INTERNAL_PASSES):
        # Clear logic flow
        if not _perform_internal_resolution_pass(config):
            break
    
    return TOPLConfig(config)
```

#### Type Hints

Use comprehensive type hints:

```python
from __future__ import annotations

from typing import Any, Generator
from collections.abc import Mapping

# Use modern union syntax (Python 3.10+)
def process_value(value: str | int | None) -> str:
    """Process configuration value."""
    return str(value) if value is not None else ""

# Proper generic types
def iter_items(data: Mapping[str, Any]) -> Generator[tuple[str, Any], None, None]:
    """Iterate over mapping items."""
    yield from data.items()
```

#### Error Handling

Implement robust error handling:

```python
from topl.exceptions import PlaceholderResolutionError

def risky_operation(data: dict[str, Any]) -> str:
    """Perform operation that might fail."""
    try:
        return process_data(data)
    except KeyError as e:
        raise PlaceholderResolutionError(
            f"Missing required key: {e}"
        ) from e
    except ValueError as e:
        raise PlaceholderResolutionError(
            f"Invalid value format: {e}"
        ) from e
```

## Extending TOPL

### 1. Adding New Features

#### Example: Custom Placeholder Syntax

```python
# src/topl/extensions.py
import re
from typing import Pattern

class CustomPlaceholderResolver:
    """Support for custom placeholder syntax."""
    
    def __init__(self, pattern: str = r'\$\{([^}]+)\}'):
        self.pattern: Pattern[str] = re.compile(pattern)
    
    def resolve(self, text: str, params: dict[str, str]) -> str:
        """Resolve custom placeholders in text."""
        def replacer(match: re.Match[str]) -> str:
            key = match.group(1).strip()
            return params.get(key, match.group(0))
        
        return self.pattern.sub(replacer, text)
```

#### Example: New Configuration Sources

```python
# src/topl/sources.py
from pathlib import Path
from typing import Any
import json

def load_json_config(path: Path) -> dict[str, Any]:
    """Load configuration from JSON file."""
    with path.open() as f:
        return json.load(f)

def load_yaml_config(path: Path) -> dict[str, Any]:
    """Load configuration from YAML file."""
    import yaml
    with path.open() as f:
        return yaml.safe_load(f)
```

### 2. Plugin System (Future)

Design considerations for plugin architecture:

```python
# Future plugin interface
from abc import ABC, abstractmethod

class PlaceholderPlugin(ABC):
    """Base class for placeholder plugins."""
    
    @abstractmethod
    def resolve(self, placeholder: str, context: dict[str, Any]) -> str | None:
        """Resolve a placeholder or return None if not handled."""
        pass
    
    @abstractmethod
    def priority(self) -> int:
        """Return plugin priority (higher = earlier execution)."""
        pass
```

## Release Process

### 1. Preparing Release

1. **Update CHANGELOG.md** with new features and fixes
2. **Ensure all tests pass** on all supported Python versions
3. **Update documentation** if needed
4. **Review security** with `bandit`

### 2. Creating Release

```bash
# Create release tag
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3

# Automated release will:
# - Build package
# - Run tests
# - Upload to PyPI
# - Create GitHub release
```

### 3. Post-Release

1. **Verify PyPI upload** - check package is available
2. **Test installation** from PyPI
3. **Update documentation** website
4. **Announce release** in relevant channels

## Getting Help

### Development Questions

- **GitHub Discussions** - For general development questions
- **GitHub Issues** - For bugs and specific problems  
- **Discord/Slack** - Real-time development chat (if available)

### Useful Resources

- **Python Type Hints** - [PEP 484](https://peps.python.org/pep-0484/)
- **Testing Best Practices** - [pytest documentation](https://pytest.org/)
- **Code Style** - [PEP 8](https://peps.python.org/pep-0008/)
- **TOML Specification** - [TOML v1.0.0](https://toml.io/en/v1.0.0)

## Recognition

Contributors are recognized in:

- **CHANGELOG.md** - Credit for specific contributions
- **README.md** - Contributors section
- **GitHub Contributors** - Automatic recognition
- **Release Notes** - Major contributions highlighted

## Thank You!

Your contributions make TOPL better for everyone. Whether you're:

- Reporting bugs
- Suggesting features  
- Writing code
- Improving documentation
- Helping other users

Every contribution is valuable and appreciated! 🙏

## Quick Reference

### Development Commands
```bash
# Setup
uv sync --all-extras
pre-commit install

# Quality checks  
uv run pytest
uv run mypy src tests
uv run ruff check .

# Build docs
cd src_docs && mkdocs serve
```

### PR Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All checks pass
- [ ] Clear commit messages