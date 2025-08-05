# Chapter 1: Getting Started

Welcome to TOPL! This chapter introduces you to the core concepts and gets you up and running with your first placeholder resolution example.

## What is TOPL?

TOPL (TOML extended with placeholders) is a Python package that brings dynamic capabilities to standard TOML configuration files. It allows you to:

- **Reference values within the same file** using `${section.key}` syntax
- **Inject external parameters** using `${parameter}` syntax  
- **Resolve placeholders in two phases** for maximum flexibility
- **Maintain full TOML compatibility** while adding powerful templating

## Core Concepts

### Placeholders

TOPL uses `${...}` syntax for placeholders:

```toml
# Internal reference - resolved from within the same file
database_url = "postgresql://localhost:5432/${database.name}"

# External parameter - provided by user
api_key = "${API_KEY}"
```

### Two-Phase Resolution

TOPL resolves placeholders in two distinct phases:

1. **Phase 1 (Internal)**: Resolves references to keys within the same TOML structure
2. **Phase 2 (External)**: Resolves remaining placeholders using user-provided parameters

This approach ensures predictable resolution order and prevents conflicts between internal and external references.

## Your First Example

Let's create a simple configuration file and resolve its placeholders.

### Step 1: Create a TOML file

Create `app-config.toml`:

```toml
[app]
name = "MyApplication"
version = "1.0.0"
debug = true

[database]
host = "localhost"
port = 5432
name = "myapp_db"
# Internal reference using ${section.key}
url = "postgresql://${database.host}:${database.port}/${database.name}"

[api]
# External parameter using ${param}
key = "${API_KEY}"
# Mixed: internal reference + external parameter
endpoint = "https://${api.host}/v1"
host = "${API_HOST}"

[logging]
# Conditional-like logic using internal references
level = "${app.debug}"
```

### Step 2: Resolve using CLI

```bash
# Provide external parameters
topl app-config.toml --API_KEY "your-secret-key" --API_HOST "api.example.com"
```

### Step 3: View the output

```python
{
  'app': {
    'name': 'MyApplication', 
    'version': '1.0.0', 
    'debug': True
  },
  'database': {
    'host': 'localhost', 
    'port': 5432, 
    'name': 'myapp_db',
    'url': 'postgresql://localhost:5432/myapp_db'  # ← Resolved internally
  },
  'api': {
    'key': 'your-secret-key',        # ← Resolved externally
    'endpoint': 'https://api.example.com/v1',  # ← Mixed resolution
    'host': 'api.example.com'        # ← Resolved externally
  },
  'logging': {
    'level': True                     # ← Internal reference to app.debug
  }
}
```

## Understanding the Resolution Process

Let's trace what happened:

### Phase 1: Internal Resolution
- `${database.host}` → `"localhost"` (from `database.host`)
- `${database.port}` → `5432` (from `database.port`) 
- `${database.name}` → `"myapp_db"` (from `database.name`)
- `${app.debug}` → `True` (from `app.debug`)

Result: `database.url` becomes `"postgresql://localhost:5432/myapp_db"`

### Phase 2: External Resolution
- `${API_KEY}` → `"your-secret-key"` (from CLI parameter)
- `${API_HOST}` → `"api.example.com"` (from CLI parameter)

Result: `api.key` and `api.host` get their final values

## Common Use Cases

### Environment-Specific Configuration

```toml
[database]
host = "localhost"
port = 5432
name = "${DB_NAME}"
user = "${DB_USER}"
password = "${DB_PASSWORD}"
url = "postgresql://${database.user}:${database.password}@${database.host}:${database.port}/${database.name}"
```

### Template Reuse

```toml
[defaults]
protocol = "https"
domain = "example.com"
version = "v1"

[api]
base_url = "${defaults.protocol}://${defaults.domain}"
users_endpoint = "${api.base_url}/${defaults.version}/users"
posts_endpoint = "${api.base_url}/${defaults.version}/posts"
```

### Multi-Environment Setup

```toml
[environments.dev]
debug = true
db_host = "localhost"

[environments.prod]  
debug = false
db_host = "prod-db.example.com"

[app]
debug_mode = "${environments.${ENVIRONMENT}.debug}"
database_host = "${environments.${ENVIRONMENT}.db_host}"
```

## Key Benefits

1. **DRY Configuration**: Define values once, reference everywhere
2. **Environment Flexibility**: Same config file, different parameter values
3. **Type Preservation**: TOML types (strings, numbers, booleans) are maintained
4. **Error Detection**: Clear warnings for unresolved placeholders
5. **Circular Reference Protection**: Automatic detection prevents infinite loops

## What's Next?

Now that you understand the basics:

- **Ready to install?** → [Chapter 2: Installation & Setup](02-installation-setup.md)
- **Want to explore syntax?** → [Chapter 3: Basic Usage](03-basic-usage.md)  
- **Need real examples?** → [Chapter 7: Configuration & Examples](07-configuration-examples.md)

## Quick Reference

### Placeholder Syntax
- `${section.key}` - Internal reference
- `${parameter}` - External parameter
- Case-sensitive, dotted notation supported

### CLI Usage
```bash
topl <file.toml> [--param1 value1] [--param2 value2]
```

### Python API Preview
```python
import tomllib
from topl import resolve_placeholders

with open('config.toml', 'rb') as f:
    data = tomllib.load(f)
    
config = resolve_placeholders(data, API_KEY="secret", DB_HOST="localhost")
print(config.database.url)  # Access resolved values
```