# Chapter 8: Troubleshooting

Common issues, debugging techniques, and solutions for TOPL-related problems.

## Common Issues

### 1. Unresolved Placeholders

**Symptom**: Placeholders remain in output as `${parameter}`

```bash
$ topl config.toml --API_KEY secret
{
  "database": {
    "url": "postgresql://localhost:5432/${DB_NAME}"  # ← Still has placeholder
  }
}
[WARNING] Could not resolve 1 placeholder(s): ${DB_NAME}
```

**Causes & Solutions**:

#### Missing External Parameter
```bash
# Problem: DB_NAME not provided
topl config.toml --API_KEY secret

# Solution: Provide missing parameter
topl config.toml --API_KEY secret --DB_NAME myapp_db
```

#### Typo in Parameter Name
```toml
# config.toml
database_name = "${DB_NANE}"  # ← Typo: NANE instead of NAME
```

```bash
# Problem: Parameter name mismatch
topl config.toml --DB_NAME myapp

# Solution: Fix typo in TOML file or CLI
topl config.toml --DB_NANE myapp  # Match the typo, or fix TOML
```

#### Case Sensitivity Issues
```toml
# config.toml
api_key = "${api_key}"  # ← lowercase
```

```bash
# Problem: Case mismatch
topl config.toml --API_KEY secret

# Solution: Match case exactly
topl config.toml --api_key secret
```

### 2. Circular Reference Errors

**Symptom**: `CircularReferenceError` exception

```toml
# Problematic config.toml
[section_a]
value = "${section_b.value}"

[section_b]  
value = "${section_a.value}"
```

**Error**:
```
CircularReferenceError: Reached maximum internal passes (10). 
Circular placeholder references detected.
```

**Solutions**:

#### Identify the Cycle
Use verbose mode to see resolution steps:
```bash
topl config.toml --verbose
```

Look for repeating patterns in the debug output.

#### Break the Cycle
```toml
# Solution 1: Provide a base value
[section_a]
base_value = "hello"
value = "${section_a.base_value} ${section_b.suffix}"

[section_b]
suffix = "world"
```

#### Use External Parameters
```toml
# Solution 2: Break cycle with external parameter
[section_a]
value = "${INITIAL_VALUE} ${section_b.suffix}"

[section_b]
suffix = "processed"
```

### 3. File and Path Issues

**Symptom**: File not found or permission errors

```bash
$ topl missing-config.toml
Error: TOML file missing-config.toml not found
Exit code: 1
```

**Solutions**:

#### Check File Path
```bash
# Use absolute path
topl /full/path/to/config.toml

# Or ensure you're in the right directory
ls -la config.toml
topl config.toml
```

#### Fix File Permissions
```bash
# Check permissions
ls -la config.toml

# Fix if necessary
chmod 644 config.toml
```

#### Verify TOML Syntax
```bash
# Use a TOML validator
python -c "import tomllib; print('Valid TOML')" < config.toml
```

### 4. Type Conversion Issues

**Symptom**: Unexpected string values instead of numbers/booleans

```toml
# config.toml
[app]
port = "${PORT}"  # Expected: integer
debug = "${DEBUG}" # Expected: boolean
```

```bash
$ topl config.toml --PORT 8080 --DEBUG true
{
  "app": {
    "port": "8080",    # ← String instead of integer
    "debug": "true"    # ← String instead of boolean
  }
}
```

**Cause**: All external parameters are strings by default.

**Solutions**:

#### Provide Proper Types in TOML
```toml
# Solution 1: Use default values with correct types
[app]
port = 8080  # Default integer
debug = true # Default boolean

# Override only when needed
actual_port = "${PORT}"      # Will be string
actual_debug = "${DEBUG}"    # Will be string
```

#### Handle in Application Code
```python
# Solution 2: Convert in application
config = resolve_placeholders(data, PORT="8080", DEBUG="true")

# Convert strings to appropriate types
port = int(config.app.port)
debug = config.app.debug.lower() == 'true'
```

### 5. Nested Reference Issues

**Symptom**: Complex nested references don't resolve properly

```toml
# config.toml
[environments.${ENVIRONMENT}]
database_host = "localhost"

[app]
db_host = "${environments.${ENVIRONMENT}.database_host}"  # ← Complex nesting
```

**Problem**: External parameters in path references aren't resolved in Phase 1.

**Solutions**:

#### Restructure Configuration
```toml
# Solution 1: Flatten structure
[environments.development]
database_host = "localhost"

[environments.production]  
database_host = "prod.example.com"

[app]
environment = "${ENVIRONMENT}"
# This won't work directly, need external resolution first
```

#### Use Two-Step Resolution
```python
# Solution 2: Handle in code
import tomllib
from topl import resolve_placeholders

with open('config.toml', 'rb') as f:
    data = tomllib.load(f)

# First resolve ENVIRONMENT
config = resolve_placeholders(data, ENVIRONMENT="development")

# Now internal references can resolve
# db_host will resolve to environments.development.database_host
```

## Debugging Techniques

### 1. Verbose Mode

Enable detailed logging to see resolution steps:

```bash
topl config.toml --verbose --API_KEY test
```

Sample verbose output:
```
[DEBUG] Starting internal placeholder resolution
[DEBUG] Resolved internal: ${database.host} -> localhost
[DEBUG] Resolved internal: ${database.port} -> 5432
[DEBUG] Internal resolution stabilized after 2 passes
[DEBUG] Starting external placeholder resolution with 1 parameters
[DEBUG] Resolved external: ${API_KEY} -> test
[DEBUG] All placeholders resolved successfully
```

### 2. Step-by-Step Resolution

Create a test file to isolate issues:

```toml
# debug.toml - Minimal test case
[test]
simple = "${SIMPLE_PARAM}"
internal = "${test.base}"  
base = "hello"
```

```bash
topl debug.toml --verbose --SIMPLE_PARAM world
```

### 3. Python Debugging

Use Python for detailed inspection:

```python
import tomllib
from topl import resolve_placeholders
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

with open('config.toml', 'rb') as f:
    data = tomllib.load(f)

print("Original data:")
print(data)

config = resolve_placeholders(data, API_KEY="test")

print("\nResolved config:")
print(config.to_dict())

print(f"\nUnresolved placeholders: {config.unresolved_placeholders}")
```

### 4. Check Resolution Phases

Test internal and external resolution separately:

```python
# Test internal resolution only
config_internal = resolve_placeholders(data)  # No external params
print("After internal resolution:", config_internal.unresolved_placeholders)

# Test with external params
config_full = resolve_placeholders(data, **external_params)
print("After external resolution:", config_full.unresolved_placeholders)
```

## Performance Issues

### 1. Slow Resolution

**Symptom**: TOPL takes too long to resolve large configurations

**Diagnosis**:
```python
import time
from topl import resolve_placeholders

start = time.time()
config = resolve_placeholders(large_data, **params)
print(f"Resolution took {time.time() - start:.2f} seconds")
```

**Solutions**:

#### Reduce Complexity
```toml
# Avoid deeply nested references
[level1.level2.level3.level4]
value = "${level1.level2.level3.level4.deep_value}"  # ← Too deep

# Prefer flatter structures
[config]
deep_value = "value"
reference = "${config.deep_value}"  # ← Better
```

#### Limit Reference Chains
```toml
# Avoid long chains
[a]
value = "${b.value}"

[b] 
value = "${c.value}"

[c]
value = "${d.value}"  # ← Long chain

# Prefer direct references
[config]
base = "value"
derived1 = "${config.base}"
derived2 = "${config.base}"  # ← Direct references
```

### 2. Memory Usage

**Symptom**: High memory consumption with large configs

**Diagnosis**:
```python
import tracemalloc
from topl import resolve_placeholders

tracemalloc.start()
config = resolve_placeholders(data, **params)
current, peak = tracemalloc.get_traced_memory()
print(f"Memory: {current / 1024 / 1024:.1f}MB (peak: {peak / 1024 / 1024:.1f}MB)")
```

**Solutions**:

#### Process in Chunks
```python
# For very large configurations, process sections separately
sections = ['database', 'api', 'cache']
configs = {}

for section in sections:
    section_data = {section: data[section]}
    configs[section] = resolve_placeholders(section_data, **params)
```

#### Clear Unused Data
```python
# Clear references to original data
config = resolve_placeholders(data, **params)
del data  # Free original data
```

## Error Messages Reference

### Exit Codes

| Code | Error Type | Description | Solution |
|------|------------|-------------|----------|
| 0 | Success | All placeholders resolved | - |
| 1 | File Error | File not found/invalid | Check file path and permissions |
| 2 | Resolution Error | Circular references/resolution failure | Fix circular references |
| 3 | Parameter Error | Invalid parameters | Check parameter names and values |

### Common Error Messages

#### "TOML file not found"
```
Error: TOML file config.toml not found
```
- Check file path spelling
- Verify file exists: `ls -la config.toml`
- Use absolute path if needed

#### "Invalid TOML"
```
Error: Invalid TOML in config.toml: Expected '=' after key name
```
- Validate TOML syntax
- Check for missing quotes, brackets, or commas
- Use online TOML validator

#### "Circular placeholder references detected"
```
Error: Reached maximum internal passes (10). Circular placeholder references detected.
```
- Identify circular dependencies
- Use `--verbose` to trace resolution steps
- Break cycles with external parameters or base values

#### "Could not resolve placeholder(s)"
```
Warning: Could not resolve 2 placeholder(s): ${API_KEY}, ${DB_HOST}
```
- Provide missing external parameters
- Check parameter name spelling and case
- Verify parameter is actually needed

## Getting Help

### 1. Check Documentation
- Read relevant chapters for your use case
- Review examples in [Chapter 7](07-configuration-examples.md)
- Check [API Reference](06-api-reference.md) for Python usage

### 2. Search Issues
Visit [GitHub Issues](https://github.com/terragonlabs/topl/issues) and search for similar problems.

### 3. Create Minimal Example

When reporting issues, create a minimal reproduction case:

```toml
# minimal-repro.toml
[test]
value = "${PARAM}"
```

```bash
# Command that fails
topl minimal-repro.toml --PARAM test
```

### 4. Report Bugs

Include in your bug report:
- TOPL version: `topl --version`
- Python version: `python --version`
- Operating system
- Complete error message
- Minimal reproduction case
- Expected vs actual behavior

## Quick Troubleshooting Checklist

- [ ] **File exists and is readable**
- [ ] **TOML syntax is valid**
- [ ] **All external parameters provided**
- [ ] **Parameter names match exactly (case-sensitive)**
- [ ] **No circular references in internal placeholders**
- [ ] **Complex nested references are structured correctly**
- [ ] **Used `--verbose` for debugging complex issues**

## What's Next?

- **Want to contribute?** → [Chapter 9: Development & Contributing](09-development-contributing.md)
- **Need more examples?** → [Chapter 7: Configuration & Examples](07-configuration-examples.md)
- **Review the API?** → [Chapter 6: API Reference](06-api-reference.md)