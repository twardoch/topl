---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Create config file with content: '...'
2. Run command: `topl config.toml --param value`
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened instead.

**Minimal reproduction case**
Please provide the smallest possible TOML file and command that reproduces the issue:

```toml
# config.toml
[section]
value = "${PARAM}"
```

```bash
topl config.toml --PARAM test
```

**Environment (please complete the following information):**
- OS: [e.g. Ubuntu 22.04, Windows 11, macOS 13]
- Python version: [e.g. 3.11.5]
- TOPL version: [e.g. 1.2.3]
- Installation method: [e.g. pip, uv, from source]

**Error output**
If applicable, add the complete error message:

```
Error message here
```

**Additional context**
Add any other context about the problem here.