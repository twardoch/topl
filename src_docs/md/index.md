# TOPL Documentation

**TOML extended with placeholders** - A powerful Python package for dynamic TOML configuration files with two-phase placeholder resolution.

## Quick Overview (TLDR)

TOPL extends standard TOML files with placeholder functionality, allowing you to create dynamic, reusable configuration files. It resolves placeholders in two phases:

1. **Internal Phase**: Resolves `${section.key}` references within the same TOML file
2. **External Phase**: Resolves `${param}` with user-supplied parameters

```toml
# config.toml
[database]
host = "localhost"
port = 5432
url = "postgresql://${username}:${password}@${database.host}:${database.port}/${dbname}"

[app]
name = "MyApp"
debug_mode = true
log_level = "${app.debug_mode ? 'DEBUG' : 'INFO'}"
```

```bash
topl config.toml --username admin --password secret --dbname mydb
```

## Documentation Chapters

### [Chapter 1: Getting Started](01-getting-started.md)
**What you'll learn**: Quick introduction to TOPL concepts, basic workflow, and your first placeholder resolution example.

**Key topics**: Core concepts, installation verification, "Hello World" example

---

### [Chapter 2: Installation & Setup](02-installation-setup.md)
**What you'll learn**: Complete installation guide across different environments, dependency management, and development setup.

**Key topics**: pip/uv installation, virtual environments, development dependencies, verification steps

---

### [Chapter 3: Basic Usage](03-basic-usage.md)
**What you'll learn**: Fundamental TOPL usage patterns, placeholder syntax, and common use cases.

**Key topics**: Placeholder syntax, file structure, CLI basics, Python API introduction

---

### [Chapter 4: Two-Phase Resolution System](04-two-phase-resolution.md)
**What you'll learn**: Deep dive into TOPL's core feature - the two-phase resolution system that handles internal references and external parameters.

**Key topics**: Internal resolution mechanics, external parameter injection, resolution order, circular reference handling

---

### [Chapter 5: CLI Reference](05-cli-reference.md)
**What you'll learn**: Complete command-line interface documentation with all options, flags, and usage patterns.

**Key topics**: Command syntax, parameter passing, output formats, advanced CLI features

---

### [Chapter 6: API Reference](06-api-reference.md)
**What you'll learn**: Comprehensive Python API documentation for programmatic usage in your applications.

**Key topics**: Core functions, classes, type hints, error handling, integration examples

---

### [Chapter 7: Configuration & Examples](07-configuration-examples.md)
**What you'll learn**: Real-world configuration examples and advanced patterns for complex scenarios.

**Key topics**: Database configurations, multi-environment setups, template patterns, best practices

---

### [Chapter 8: Troubleshooting](08-troubleshooting.md)
**What you'll learn**: Common issues, debugging techniques, and solutions to typical problems.

**Key topics**: Error diagnosis, circular references, performance issues, debugging tips

---

### [Chapter 9: Development & Contributing](09-development-contributing.md)
**What you'll learn**: How to contribute to TOPL, development setup, testing, and extending functionality.

**Key topics**: Development environment, testing framework, code style, contribution guidelines

---

## Quick Navigation

- **New to TOPL?** Start with [Getting Started](01-getting-started.md)
- **Ready to install?** Jump to [Installation & Setup](02-installation-setup.md)
- **Need examples?** Check [Configuration & Examples](07-configuration-examples.md)
- **Having issues?** See [Troubleshooting](08-troubleshooting.md)
- **Want to contribute?** Read [Development & Contributing](09-development-contributing.md)

## Features at a Glance

- ✅ **Two-phase resolution**: Internal references first, then external parameters
- ✅ **Circular reference detection**: Prevents infinite loops with clear error messages
- ✅ **Type-safe**: Full type hints and mypy compatibility
- ✅ **Rich CLI**: Beautiful command-line interface with helpful output
- ✅ **Python 3.11+**: Modern Python with latest features
- ✅ **Zero breaking changes**: Drop-in replacement for standard TOML loading
- ✅ **Comprehensive testing**: 95%+ test coverage with unit and integration tests

## Support

- **GitHub Repository**: [terragonlabs/topl](https://github.com/terragonlabs/topl)
- **Issue Tracker**: [Report bugs or request features](https://github.com/terragonlabs/topl/issues)
- **Changelog**: [View release history](https://github.com/terragonlabs/topl/blob/main/CHANGELOG.md)