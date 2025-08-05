# Chapter 2: Installation & Setup

This chapter covers everything you need to install and configure TOPL in different environments, from simple pip installations to full development setups.

## System Requirements

- **Python**: 3.11 or higher
- **Operating System**: Linux, macOS, Windows
- **Memory**: Minimal requirements (< 50MB)
- **Dependencies**: Automatically managed

## Installation Methods

### Method 1: pip (Recommended)

The simplest way to install TOPL:

```bash
pip install toml-topl
```

### Method 2: uv (Fastest)

Using [uv](https://github.com/astral-sh/uv) for faster package management:

```bash
uv add toml-topl
```

### Method 3: From Source

For the latest development version:

```bash
pip install git+https://github.com/terragonlabs/topl.git
```

## Virtual Environment Setup

### Using venv (Standard)

```bash
# Create virtual environment
python -m venv topl-env

# Activate (Linux/macOS)
source topl-env/bin/activate

# Activate (Windows)
topl-env\Scripts\activate

# Install TOPL
pip install toml-topl
```

### Using uv (Recommended)

```bash
# Create and activate environment in one step
uv venv --python 3.11
uv add toml-topl
```

## Verification

### Command Line Verification

After installation, verify TOPL is working:

```bash
# Check version
topl --version

# Test basic functionality
echo 'message = "Hello ${name}!"' > test.toml
topl test.toml --name "World"
```

Expected output:
```python
{'message': 'Hello World!'}
```

### Python API Verification

```python
import topl
print(topl.__version__)

# Test basic resolution
import tomllib
from topl import resolve_placeholders

data = tomllib.loads('greeting = "Hello ${name}!"')
config = resolve_placeholders(data, name="TOPL")
print(config.greeting)  # Output: Hello TOPL!
```

## IDE Integration

### VS Code

Install recommended extensions for better TOML editing:

```json
{
  "recommendations": [
    "tamasfe.even-better-toml",
    "ms-python.python"
  ]
}
```

Add to your VS Code settings:

```json
{
  "files.associations": {
    "*.topl": "toml"
  }
}
```

### PyCharm

1. Install the TOML plugin
2. Associate `.topl` files with TOML syntax highlighting
3. Configure Python interpreter to include TOPL package

## Development Installation

For contributing to TOPL or using development features:

### Prerequisites

- Git
- Python 3.11+
- uv (recommended) or pip

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/terragonlabs/topl.git
cd topl

# Install with all development dependencies
uv sync --all-extras

# Or with pip
pip install -e ".[dev,docs,test]"
```

### Development Dependencies

The development installation includes:

| Category | Purpose | Key Packages |
|----------|---------|--------------|
| **Testing** | Unit & integration tests | pytest, pytest-cov, hypothesis |
| **Linting** | Code quality | ruff, mypy, bandit |
| **Documentation** | Docs generation | mkdocs, mkdocs-material |
| **Development** | Pre-commit hooks | pre-commit |

### Pre-commit Hooks

Set up automatic code quality checks:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Configuration Files

### Global Configuration

TOPL respects standard Python configuration patterns:

```bash
# Linux/macOS
~/.config/topl/config.toml

# Windows  
%APPDATA%\topl\config.toml
```

Example global config:

```toml
[defaults]
verbose = false
output_format = "json"

[logging]
level = "INFO"
colorize = true
```

### Project Configuration

For project-specific settings, create `pyproject.toml`:

```toml
[tool.topl]
default_external_file = "env.toml"
max_internal_passes = 10
warn_unresolved = true
```

## Docker Usage

### Using Official Python Image

```dockerfile
FROM python:3.11-slim

RUN pip install toml-topl

COPY config.toml .
RUN topl config.toml --env production
```

### Multi-stage Build

```dockerfile
# Build stage
FROM python:3.11 as builder
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Runtime stage  
FROM python:3.11-slim
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .
CMD ["topl", "config.toml"]
```

## Environment Variables

TOPL respects these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `TOPL_VERBOSE` | `false` | Enable verbose logging |
| `TOPL_CONFIG_PATH` | - | Default config file path |
| `TOPL_MAX_PASSES` | `10` | Maximum internal resolution passes |
| `TOPL_LOG_LEVEL` | `INFO` | Logging level |

Example usage:

```bash
TOPL_VERBOSE=true topl config.toml --env production
```

## Platform-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Path separators: use forward slashes or escape backslashes
- Environment variables: `$env:VARIABLE_NAME`

```powershell
$env:API_KEY = "secret"
topl config.toml --environment production
```

### macOS

- Homebrew Python recommended: `brew install python@3.11`
- Xcode Command Line Tools may be required

### Linux

- Most distributions include compatible Python
- Ubuntu/Debian: `apt install python3.11 python3.11-venv`
- CentOS/RHEL: `dnf install python3.11`

## Performance Optimization

### Large Files

For configuration files > 100KB:

```bash
# Use streaming mode (future feature)
topl --stream large-config.toml

# Parallel processing
topl --parallel config.toml
```

### Memory Usage

Monitor memory with complex configurations:

```python
import tracemalloc
tracemalloc.start()

# Your TOPL code here
config = resolve_placeholders(data, **params)

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.1f} MB")
print(f"Peak: {peak / 1024 / 1024:.1f} MB")
```

## Troubleshooting Installation

### Common Issues

#### ModuleNotFoundError

```bash
# Solution: Verify installation
pip show toml-topl

# Reinstall if necessary
pip uninstall toml-topl
pip install toml-topl
```

#### Permission Errors

```bash
# Use user installation
pip install --user toml-topl

# Or use virtual environment (recommended)
python -m venv env
source env/bin/activate
pip install toml-topl
```

#### Version Conflicts

```bash
# Check dependency conflicts
pip check

# Use compatible versions
pip install "toml-topl>=1.0.0,<2.0.0"
```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](08-troubleshooting.md)
2. Search [existing issues](https://github.com/terragonlabs/topl/issues)
3. Create a [new issue](https://github.com/terragonlabs/topl/issues/new) with:
   - Python version (`python --version`)
   - TOPL version (`topl --version`)
   - Operating system
   - Full error message
   - Minimal reproduction example

## What's Next?

Now that TOPL is installed:

- **Learn the basics** → [Chapter 3: Basic Usage](03-basic-usage.md)
- **Understand resolution** → [Chapter 4: Two-Phase Resolution System](04-two-phase-resolution.md)
- **See examples** → [Chapter 7: Configuration & Examples](07-configuration-examples.md)

## Quick Reference

### Installation Commands
```bash
# Standard
pip install toml-topl

# Development
git clone https://github.com/terragonlabs/topl.git
cd topl && uv sync --all-extras

# Verification
topl --version
```

### Essential Files
- `~/.config/topl/config.toml` - Global configuration
- `pyproject.toml` - Project configuration
- `.env` - Environment variables (if using python-dotenv)