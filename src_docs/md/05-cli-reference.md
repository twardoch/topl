# Chapter 5: CLI Reference

Complete reference for the TOPL command-line interface, covering all options, parameters, and usage patterns.

## Basic Syntax

```bash
topl [OPTIONS] <config-file> [--param value] [--param value] ...
```

## Core Commands

### Primary Command

```bash
topl config.toml
```

Loads and resolves `config.toml` with default settings.

### With Parameters

```bash
topl config.toml --API_KEY "your-key" --ENVIRONMENT "production"
```

Resolves placeholders using provided external parameters.

## Command Line Options

### Global Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--verbose` | `-v` | Enable verbose output | `false` |
| `--help` | `-h` | Show help message | - |
| `--version` | | Show version | - |

### Output Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | Output format: `json`, `yaml`, `toml` | `json` |
| `--pretty` | Pretty-print output | `true` |
| `--no-color` | Disable colored output | `false` |

### Resolution Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-passes` | Maximum internal resolution passes | `10` |
| `--strict` | Fail on unresolved placeholders | `false` |
| `--warn-unresolved` | Warn about unresolved placeholders | `true` |

## Parameter Passing

### Basic Parameters

```bash
# String parameters
topl config.toml --API_KEY "sk-abc123" --HOST "localhost"

# Numeric parameters (auto-detected)
topl config.toml --PORT "8080" --TIMEOUT "30.5"

# Boolean parameters
topl config.toml --DEBUG "true" --PRODUCTION "false"
```

### Environment Variables

TOPL can read parameters from environment variables:

```bash
# Set environment variables
export API_KEY="your-secret-key"
export DB_HOST="localhost"

# Use in TOPL (parameters take precedence over env vars)
topl config.toml --ENVIRONMENT "development"
```

### Parameter Files

Load parameters from external files:

```bash
# params.toml
API_KEY = "your-key"
DB_HOST = "localhost"
DEBUG = true

# Use parameter file
topl config.toml @params.toml
```

## Output Formats

### JSON (Default)

```bash
topl config.toml --API_KEY "test"
```

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "url": "postgresql://localhost:5432/myapp"
  },
  "api": {
    "key": "test"
  }
}
```

### YAML Output

```bash
topl config.toml --format yaml --API_KEY "test"
```

```yaml
database:
  host: localhost
  port: 5432
  url: postgresql://localhost:5432/myapp
api:
  key: test
```

### TOML Output

```bash
topl config.toml --format toml --API_KEY "test"
```

```toml
[database]
host = "localhost"
port = 5432
url = "postgresql://localhost:5432/myapp"

[api]
key = "test"
```

## Advanced Usage

### Verbose Mode

```bash
topl config.toml --verbose --API_KEY "test"
```

Shows detailed resolution process:

```
[DEBUG] Starting internal placeholder resolution
[DEBUG] Resolved internal: ${database.host} -> localhost
[DEBUG] Internal resolution stabilized after 2 passes
[DEBUG] Starting external placeholder resolution with 1 parameters
[DEBUG] Resolved external: ${API_KEY} -> test
[DEBUG] All placeholders resolved successfully
```

### Strict Mode

```bash
topl config.toml --strict --API_KEY "test"
```

Fails if any placeholders remain unresolved:

```
Error: Unresolved placeholders found: ${DB_PASSWORD}
Exit code: 1
```

### Custom Max Passes

```bash
topl config.toml --max-passes 5 --API_KEY "test"
```

Limits internal resolution to 5 passes (useful for performance tuning).

## File Handling

### Input Files

TOPL accepts various file formats:

```bash
# Standard TOML
topl config.toml

# Alternative extensions  
topl config.topl
topl settings.tml

# Stdin input
cat config.toml | topl -
```

### Output Redirection

```bash
# Save to file
topl config.toml --API_KEY "test" > resolved-config.json

# Pipe to other commands
topl config.toml --API_KEY "test" | jq '.database.url'
```

## Error Handling

### Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `0` | Success | All placeholders resolved |
| `1` | File Error | Input file not found or invalid |
| `2` | Resolution Error | Circular references or resolution failure |
| `3` | Parameter Error | Invalid parameters or missing required values |
| `4` | Format Error | Invalid output format specified |

### Error Examples

#### File Not Found

```bash
$ topl missing.toml
Error: TOML file missing.toml not found
Exit code: 1
```

#### Circular Reference

```bash
$ topl circular.toml
Error: Circular placeholder references detected after 10 passes
Exit code: 2
```

#### Invalid Format

```bash
$ topl config.toml --format xml
Error: Unsupported output format: xml
Valid formats: json, yaml, toml
Exit code: 4
```

## Configuration Files

### Global Configuration

Create `~/.config/topl/config.toml`:

```toml
[cli]
default_format = "yaml"
verbose = false
max_passes = 10

[output]
pretty = true
color = true
```

### Project Configuration

Create `.topl.toml` in your project root:

```toml
[parameters]
# Default parameter values
ENVIRONMENT = "development"
DEBUG = "true"

[resolution] 
max_passes = 15
strict = false
```

## Scripting and Automation

### Bash Integration

```bash
#!/bin/bash

# Resolve configuration
CONFIG=$(topl app.toml --ENVIRONMENT "$ENV" --API_KEY "$API_KEY")

# Extract specific values
DB_URL=$(echo "$CONFIG" | jq -r '.database.url')
API_ENDPOINT=$(echo "$CONFIG" | jq -r '.api.endpoint')

# Use in your application
./my-app --db-url "$DB_URL" --api-endpoint "$API_ENDPOINT"
```

### Make Integration

```makefile
# Makefile
CONFIG_FILE = config.toml
ENVIRONMENT ?= development

resolve-config:
	topl $(CONFIG_FILE) \
		--ENVIRONMENT $(ENVIRONMENT) \
		--API_KEY $(API_KEY) \
		--format yaml > resolved-config.yaml

deploy: resolve-config
	kubectl apply -f resolved-config.yaml
```

### Docker Integration

```dockerfile
FROM python:3.11-slim

# Install TOPL
RUN pip install toml-topl

# Copy configuration
COPY config.toml .

# Resolve at runtime
CMD topl config.toml \
    --API_KEY "$API_KEY" \
    --DB_HOST "$DB_HOST" \
    --ENVIRONMENT "$ENVIRONMENT"
```

## Performance Tips

### Large Files

```bash
# For large configurations, consider format selection
topl large-config.toml --format json --no-pretty  # Faster parsing
```

### Parallel Processing

```bash
# Process multiple configs in parallel
ls configs/*.toml | xargs -P 4 -I {} topl {} --ENVIRONMENT production
```

### Caching Results

```bash
# Cache resolved configurations
CACHE_FILE="resolved-$(date +%Y%m%d).json"
if [ ! -f "$CACHE_FILE" ]; then
    topl config.toml --ENVIRONMENT production > "$CACHE_FILE"
fi
```

## Troubleshooting Commands

### Validate Configuration

```bash
# Check for syntax errors
topl config.toml --dry-run
```

### Debug Resolution

```bash
# See all resolution steps
topl config.toml --verbose --API_KEY "test" 2>&1 | grep "Resolved"
```

### Check Unresolved Placeholders

```bash
# List unresolved placeholders
topl config.toml 2>&1 | grep "Could not resolve"
```

## Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
- name: Resolve Configuration
  run: |
    topl config.toml \
      --ENVIRONMENT ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }} \
      --API_KEY ${{ secrets.API_KEY }} \
      --DB_PASSWORD ${{ secrets.DB_PASSWORD }} \
      --format yaml > k8s-config.yaml
```

### Development Workflow

```bash
# Development
topl config.toml --ENVIRONMENT dev --DEBUG true

# Testing  
topl config.toml --ENVIRONMENT test --DEBUG false

# Production
topl config.toml --ENVIRONMENT prod --DEBUG false --strict
```

## What's Next?

- **Explore the Python API** → [Chapter 6: API Reference](06-api-reference.md)
- **See real-world examples** → [Chapter 7: Configuration & Examples](07-configuration-examples.md)
- **Need help?** → [Chapter 8: Troubleshooting](08-troubleshooting.md)

## Quick Reference Card

```bash
# Basic usage
topl config.toml --PARAM value

# Common options
topl config.toml --verbose --format yaml --PARAM value

# Multiple parameters
topl config.toml --API_KEY key --DB_HOST host --PORT 5432

# Strict mode (fail on unresolved)
topl config.toml --strict --PARAM value

# Save output
topl config.toml --PARAM value > output.json
```