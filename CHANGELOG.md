# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of TOPL (TOML Extended with Placeholders)
- Two-phase placeholder resolution (internal → external)
- Command-line interface via Fire
- Comprehensive programmatic API
- Full type hint support
- Circular reference detection
- Rich console output and logging
- 95%+ test coverage
- Modern Python packaging with uv and hatch
- GitHub Actions CI/CD workflows
- Documentation and examples

### Core Features
- `resolve_placeholders()` function for processing TOML data
- `TOPLConfig` class for enhanced configuration objects  
- Support for nested placeholder resolution
- External parameter injection
- Unresolved placeholder tracking and warnings
- Path expansion and file handling utilities

### CLI Features
- `topl` command-line tool
- `python -m topl` module execution
- Verbose logging mode
- External parameter passing
- Rich formatting for output
- Comprehensive error handling

### Development
- Modern Python 3.11+ compatibility
- PEP 621 compliant pyproject.toml
- UV package management
- Hatch build system
- Git-tag based versioning
- Ruff linting and formatting
- MyPy type checking
- Pytest testing framework
- Pre-commit hooks ready
- GitHub Actions for testing and releases

## [0.1.0] - Initial Development

### Added
- Project structure and configuration
- Core placeholder resolution engine
- CLI interface implementation
- Basic test suite
- Documentation framework

---

## Release Notes Template

For future releases, use this template:

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes