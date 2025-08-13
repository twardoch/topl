# TOPL Repository File Catalog

## Filesystem Tree Structure

```
.
├── .DS_Store                           # macOS system file (should be gitignored)
├── .github/                            # GitHub configuration directory
│   ├── dependabot.yml                  # Dependabot dependency update configuration
│   └── workflows/                      # GitHub Actions workflow definitions
│       ├── ci.yml                      # Continuous Integration workflow
│       ├── release.yml                 # Release automation workflow
│       └── test-pypi.yml               # Test PyPI publishing workflow
├── .gitignore                          # Git ignore patterns
├── .python-version                     # Python version specification for pyenv
├── CHANGELOG.md                        # Project change history documentation
├── CLAUDE.md                           # Claude Code AI assistant project instructions
├── LICENSE                             # MIT license file
├── README.md                           # Main project documentation and usage guide
├── REPORT-2025-07-24.md               # Project status report from July 24, 2025
├── REVIEW/                             # Review and analysis folder (THIS IS NEW)
│   ├── filesystem_tree.txt             # Generated filesystem listing
│   └── FILES-cla.md                    # This file - comprehensive file catalog
├── TODO.md                             # Project task list and roadmap
├── WORK.md                             # Work progress tracking and status updates
├── _github/                            # Duplicate GitHub configuration (redundant)
│   ├── ISSUE_TEMPLATE/                 # GitHub issue templates
│   │   ├── bug_report.md               # Bug report issue template
│   │   └── feature_request.md          # Feature request issue template
│   ├── PULL_REQUEST_TEMPLATE.md        # Pull request template
│   ├── dependabot.yml                  # Duplicate dependabot configuration
│   └── workflows/                      # Duplicate workflow definitions
│       ├── ci.yml                      # Duplicate CI workflow
│       ├── docs.yml                    # Documentation deployment workflow
│       └── release.yml                 # Duplicate release workflow
├── docs/                               # Documentation deployment directory
│   ├── .nojekyll                       # Disables Jekyll processing for GitHub Pages
│   └── github-actions-templates.md     # GitHub Actions templates documentation
├── issues/                             # Issue tracking and feedback storage
│   ├── 101.txt                         # Issue #101 details
│   └── 102.txt                         # Issue #102 details
├── llms.txt                            # Generated codebase snapshot for LLMs
├── pyproject.toml                      # Modern Python project configuration (PEP 621)
├── src/                                # Source code directory
│   ├── repo/                           # Empty repo package (unused)
│   │   └── __init__.py                 # Empty package initializer
│   └── topl/                           # Main TOPL package
│       ├── __init__.py                 # Package public API exports
│       ├── __main__.py                 # CLI entry point for python -m topl
│       ├── _version.py                 # Auto-generated version from git tags
│       ├── cli.py                      # Command-line interface implementation
│       ├── constants.py                # Package constants and configuration
│       ├── core.py                     # Core placeholder resolution logic
│       ├── exceptions.py               # Custom exception definitions
│       ├── py.typed                    # Type checking marker for mypy
│       ├── types.py                    # Type definitions and annotations
│       └── utils.py                    # Utility functions and helpers
├── src_docs/                           # Documentation source files
│   ├── md/                             # Markdown documentation files
│   │   ├── 01-getting-started.md       # Getting started guide
│   │   ├── 02-installation-setup.md    # Installation and setup instructions
│   │   ├── 03-basic-usage.md           # Basic usage examples
│   │   ├── 04-two-phase-resolution.md  # Two-phase resolution explanation
│   │   ├── 05-cli-reference.md         # CLI command reference
│   │   ├── 06-api-reference.md         # API reference documentation
│   │   ├── 07-configuration-examples.md # Configuration examples and patterns
│   │   ├── 08-troubleshooting.md       # Troubleshooting guide
│   │   ├── 09-development-contributing.md # Development and contribution guide
│   │   └── index.md                    # Documentation index/home page
│   └── mkdocs.yml                      # MkDocs configuration for documentation
├── tests/                              # Test suite directory
│   ├── conftest.py                     # Pytest configuration and shared fixtures
│   ├── integration/                    # Integration tests
│   │   └── test_end_to_end.py          # End-to-end workflow tests
│   └── unit/                           # Unit tests
│       ├── test_cli.py                 # CLI interface tests
│       ├── test_core.py                # Core functionality tests
│       └── test_utils.py               # Utility function tests
└── uv.lock                             # uv dependency lock file
```

## Detailed File and Folder Descriptions

### Root Level Files

**Configuration & Metadata**
- `.DS_Store`: macOS system file that tracks folder view options - should be added to .gitignore
- `.gitignore`: Specifies files and patterns for Git to ignore during version control
- `.python-version`: Specifies Python version (3.12) for pyenv version management
- `pyproject.toml`: Modern Python project configuration following PEP 621 standards
- `uv.lock`: Lockfile for uv package manager ensuring reproducible dependency installations
- `LICENSE`: MIT license terms for the project

**Documentation & Project Management**
- `README.md`: Primary project documentation with overview, installation, and usage instructions
- `CHANGELOG.md`: Chronological record of project changes, following semantic versioning
- `TODO.md`: Comprehensive project roadmap with 261+ items across 3 phases of development
- `WORK.md`: Active work progress tracking and sprint status updates
- `CLAUDE.md`: Instructions for Claude Code AI assistant on project-specific development guidelines
- `REPORT-2025-07-24.md`: Detailed project status report from July 24, 2025
- `llms.txt`: Compressed codebase snapshot generated by codetoprompt for LLM analysis

### Source Code (`src/`)

**Main Package (`src/topl/`)**
- `__init__.py`: Public API exports, version handling, and package entry point
- `__main__.py`: CLI entry point enabling `python -m topl` execution
- `_version.py`: Auto-generated version information from git tags using hatch-vcs
- `core.py`: Core placeholder resolution engine with TOPLConfig class and two-phase resolution
- `cli.py`: Fire-based command-line interface with rich output formatting
- `utils.py`: Utility functions for placeholder detection, path resolution, and string iteration
- `types.py`: Type definitions, protocols, and type aliases for the package
- `exceptions.py`: Custom exception hierarchy for domain-specific error handling
- `constants.py`: Package-wide constants including regex patterns and limits
- `py.typed`: Marker file indicating the package supports static type checking

**Unused Package (`src/repo/`)**
- `__init__.py`: Empty package initializer - appears to be unused/leftover

### Tests (`tests/`)

**Test Infrastructure**
- `conftest.py`: Pytest configuration with shared fixtures for TOML data, circular references, and temporary files

**Test Categories**
- `unit/test_core.py`: Unit tests for core placeholder resolution functionality
- `unit/test_utils.py`: Unit tests for utility functions and helpers
- `unit/test_cli.py`: Unit tests for CLI interface and command-line interactions
- `integration/test_end_to_end.py`: Integration tests for complete workflows and real-world scenarios

### GitHub Integration (`.github/`)

**Automation Workflows**
- `workflows/ci.yml`: Comprehensive CI pipeline testing across Python 3.11-3.13 on Ubuntu/macOS/Windows
- `workflows/release.yml`: Automated release process with PyPI publishing on git tag creation
- `workflows/test-pypi.yml`: Test PyPI publishing workflow for release validation
- `dependabot.yml`: Automated dependency updates for GitHub Actions and Python packages

**Issue Management**
- Issue templates and PR templates are duplicated between `.github/` and `_github/` directories

### Documentation (`src_docs/` and `docs/`)

**Source Documentation (`src_docs/`)**
- `mkdocs.yml`: MkDocs configuration for documentation site generation
- `md/`: Comprehensive documentation covering installation, usage, API reference, and development

**Deployed Documentation (`docs/`)**
- `.nojekyll`: Prevents GitHub Pages from using Jekyll processing
- `github-actions-templates.md`: GitHub Actions workflow templates and examples

### Issue Tracking (`issues/`)

**Feedback Storage**
- `101.txt`: Issue #101 content and tracking
- `102.txt`: Issue #102 content and tracking (contains Sourcery AI and Qodo Merge Pro feedback)

### Review Directory (`REVIEW/`)

**Analysis Files**
- `filesystem_tree.txt`: Generated file listing for repository structure analysis
- `FILES-cla.md`: This comprehensive file catalog and description document

### Redundancies and Cleanup Opportunities

**Duplicate Directories**
- `.github/` and `_github/` contain overlapping configurations
- Some workflows are duplicated between these directories

**Unused Components**
- `src/repo/` package appears unused and could be removed
- `.DS_Store` should be gitignored

**Missing Standard Files**
- `SECURITY.md`: Security policy and vulnerability reporting guidelines
- `CONTRIBUTING.md`: Contribution guidelines and development setup
- `.pre-commit-config.yaml`: Pre-commit hooks configuration

## Architecture Overview

The TOPL project implements a sophisticated two-phase placeholder resolution system:

1. **Phase 1**: Internal placeholder resolution within TOML structure
2. **Phase 2**: External parameter substitution from user input
3. **Phase 3**: Warning/logging for unresolved placeholders

The codebase follows modern Python packaging standards with comprehensive testing, type annotations, and automated CI/CD workflows.