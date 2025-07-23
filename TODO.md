# TODO: TOPL Package Development Specification

## Project Overview
Build a complete, production-ready Python package for TOML Extended with Placeholders (topl) that provides:
- Two-phase placeholder resolution (internal → external)
- CLI interface via Fire
- Programmatic API
- Full test coverage
- Modern Python packaging with uv/hatch
- Git-tag-based versioning with Denver
- GitHub Actions CI/CD

## Package Structure & Setup

### Core Package Infrastructure
- [ ] Create proper Python package structure with `src/topl/` layout following PEP 621
- [ ] Set up `pyproject.toml` with hatch build system and uv integration
- [ ] Initialize uv project with `uv init --package --build-backend hatchling`
- [ ] Add `src/topl/__init__.py` with version import from `_version.py`
- [ ] Create `src/topl/py.typed` marker file for type checking support
- [ ] Set up `this_file` tracking comments in all source files
- [ ] Configure `src/topl/_version.py` for dynamic versioning

### Configuration Files
- [ ] Create comprehensive `pyproject.toml` with:
  - Project metadata following PEP 621 (name="topl", dynamic=["version"])
  - Build system: `build-backend = "hatchling.build"`
  - Core dependencies: `python-box>=7.0`, `rich>=13.0`, `fire>=0.5`
  - Optional dependencies for dev: `pytest`, `ruff`, `mypy`, `coverage`
  - Tool configurations: ruff (format + lint), pytest, mypy, coverage
  - Console scripts entry point: `topl = "topl.__main__:main"`
  - Hatch version source from git tags
- [ ] Set up `.gitignore` with Python, uv, and IDE exclusions
- [ ] Generate initial `uv.lock` for reproducible development builds
- [ ] Create `.python-version` file specifying minimum Python 3.11

## Core Functionality Implementation

### Main Module Structure
- [ ] Create `src/topl/__init__.py` with public API exports
- [ ] Implement `src/topl/core.py` with:
  - `resolve_placeholders()` function (current main logic)
  - `TOPLConfig` class wrapper
  - Exception classes (`TOPLError`, `CircularReferenceError`, etc.)
- [ ] Create `src/topl/utils.py` for helper functions:
  - `_get_by_path()`
  - `_resolve_internal_once()`
  - `_resolve_external()`
  - `_iter_box_strings()`
- [ ] Implement `src/topl/constants.py` for configuration constants

### CLI Implementation
- [ ] Create `src/topl/__main__.py` with Fire-based CLI
- [ ] Implement `src/topl/cli.py` with:
  - Main CLI class with proper argument parsing
  - Verbose logging configuration
  - File I/O handling with proper error messages
  - Rich console output formatting
- [ ] Add proper CLI help documentation
- [ ] Support for configuration files and environment variables

### Type Hints & Documentation
- [ ] Add comprehensive type hints throughout codebase
- [ ] Create type aliases in `src/topl/types.py`
- [ ] Add detailed docstrings following Google/NumPy style
- [ ] Implement proper error handling with custom exceptions

## Testing Infrastructure

### Test Setup
- [ ] Create `tests/` directory with structured layout:
  - `tests/unit/` for isolated unit tests
  - `tests/integration/` for end-to-end tests
  - `tests/fixtures/` for test data (sample TOML files)
- [ ] Set up `tests/conftest.py` with reusable pytest fixtures:
  - Sample TOML data fixtures (simple, nested, circular refs)
  - Temporary file/directory fixtures
  - Mock console/logging fixtures
- [ ] Configure pytest in `pyproject.toml`:
  - Test discovery patterns, markers, coverage settings
  - Plugins: pytest-cov, pytest-mock, pytest-xdist for parallel testing

### Core Tests
- [ ] `tests/test_core.py` - Test placeholder resolution logic:
  - Internal placeholder resolution
  - External parameter substitution
  - Circular reference detection
  - Warning generation for unresolved placeholders
  - Edge cases (empty files, malformed TOML, etc.)
- [ ] `tests/test_cli.py` - Test CLI functionality:
  - Command-line argument parsing
  - File input/output
  - Error handling
  - Verbose mode
- [ ] `tests/test_utils.py` - Test utility functions
- [ ] `tests/test_integration.py` - End-to-end integration tests

### Test Coverage & Quality
- [ ] Achieve 95%+ test coverage
- [ ] Add property-based testing with hypothesis
- [ ] Create performance benchmarks
- [ ] Add mutation testing with mutmut

## Documentation

### User Documentation
- [ ] Update `README.md` with:
  - Clear project description
  - Installation instructions
  - Usage examples (CLI and programmatic)
  - API reference
  - Contributing guidelines
- [ ] Create `docs/` directory with:
  - User guide with examples
  - API documentation
  - Changelog format specification
  - Development setup guide

### Code Documentation
- [ ] Add comprehensive docstrings to all public functions
- [ ] Include usage examples in docstrings
- [ ] Document all parameters and return values
- [ ] Add type information to all docstrings

## Build & Release Infrastructure

### Version Management  
- [ ] Configure hatch-vcs for git-tag-based versioning:
  - Add `hatch-vcs` to build dependencies in `pyproject.toml`
  - Set version source: `[tool.hatch.version] source = "vcs"`
  - Configure tag pattern for semantic versioning (v*.*.*)
  - Create `_version.py` generation via hatch metadata hook
- [ ] Create version bumping workflow:
  - Script for creating release tags
  - Automated changelog generation from commits
  - Version validation in pre-commit hooks

### GitHub Actions
- [ ] Create `.github/workflows/ci.yml` for continuous integration:
  - Matrix testing: Python 3.11, 3.12, 3.13 on ubuntu-latest, macos-latest, windows-latest
  - Use `astral-sh/setup-uv@v4` action for fast dependency management
  - Run `uv sync --all-extras` for reproducible test environments
  - Code quality: `uv run ruff check && uv run ruff format --check`
  - Type checking: `uv run mypy src tests`
  - Tests: `uv run pytest --cov=topl --cov-report=xml`
  - Upload coverage to codecov.io
  - Security: `uv run bandit -r src/`
- [ ] Create `.github/workflows/release.yml` for automated releases:
  - Trigger on pushed tags matching `v*.*.*` pattern
  - Build with `uv build` (both sdist and wheel)
  - Upload to PyPI using trusted publishing (no API keys)
  - Create GitHub release with auto-generated changelog
  - Verify package installability: `uv run --with topl --from-source`
- [ ] Create `.github/workflows/test-pypi.yml` for pre-release testing
- [ ] Configure dependabot for both GitHub Actions and Python dependencies

### Build System
- [ ] Configure hatch for building:
  - Source distribution creation
  - Wheel building
  - Version management integration
- [ ] Set up pre-commit hooks:
  - Code formatting (ruff)
  - Type checking (mypy)
  - Test execution
  - Documentation checks

## Quality Assurance

### Code Quality Tools
- [ ] Configure ruff for linting and formatting
- [ ] Set up mypy for static type checking
- [ ] Add bandit for security scanning
- [ ] Configure pre-commit for automated checks

### Performance & Monitoring
- [ ] Add performance benchmarks
- [ ] Memory usage profiling
- [ ] Large file handling tests
- [ ] Stress testing for circular reference detection

## Advanced Features

### API Enhancements
- [ ] Add async support for file I/O operations
- [ ] Implement plugin system for custom placeholder resolvers
- [ ] Add configuration validation with pydantic
- [ ] Support for different output formats (JSON, YAML)

### CLI Enhancements
- [ ] Add shell completion support
- [ ] Implement configuration file support
- [ ] Add batch processing capabilities
- [ ] Rich progress bars for large files

### Error Handling & Logging
- [ ] Implement structured logging with loguru
- [ ] Add comprehensive error recovery
- [ ] Create detailed error messages with suggestions
- [ ] Add debug mode with detailed tracing

## Security & Compliance

### Security Measures
- [ ] Input validation and sanitization
- [ ] Path traversal protection
- [ ] Resource usage limits
- [ ] Security-focused code review

### Compliance
- [ ] License file (MIT/Apache 2.0)
- [ ] Security policy document
- [ ] Code of conduct
- [ ] Contributing guidelines

## Final Integration & Polish

### Integration Testing
- [ ] End-to-end workflow testing
- [ ] Cross-platform compatibility testing
- [ ] Performance regression testing
- [ ] Memory leak detection

### Release Preparation
- [ ] Final code review and refactoring
- [ ] Documentation completeness check
- [ ] Version 2.0 release preparation
- [ ] PyPI package publication
- [ ] GitHub release with comprehensive changelog

## Implementation Phases

### Phase 1: Core Infrastructure (MVP)
- [ ] Basic package structure and pyproject.toml
- [ ] Core functionality migration from original script
- [ ] Basic CLI with Fire integration
- [ ] Essential tests for core functionality
- [ ] Initial CI pipeline

### Phase 2: Quality & Documentation
- [ ] Comprehensive test suite with 95%+ coverage
- [ ] Full API documentation and type hints
- [ ] Error handling and logging improvements
- [ ] Performance optimization and benchmarking

### Phase 3: Release Preparation
- [ ] Complete GitHub Actions workflows
- [ ] Security scanning and compliance
- [ ] Final documentation polish
- [ ] v2.0 release to PyPI

## Success Criteria & Acceptance Tests
- [ ] **Functionality**: All original script features work identically
- [ ] **Quality**: 95%+ test coverage, all quality gates pass
- [ ] **Performance**: ≤10% performance regression vs original
- [ ] **Compatibility**: Works on Python 3.11+ across all major OS
- [ ] **Usability**: CLI help is clear, API is intuitive
- [ ] **Maintainability**: Code follows PEP 8, fully type-hinted
- [ ] **Automation**: Full CI/CD pipeline with automated releases
- [ ] **Distribution**: Successfully published to PyPI
- [ ] **Documentation**: Complete user and API documentation