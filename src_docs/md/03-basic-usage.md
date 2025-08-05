# Chapter 3: Basic Usage

This chapter covers the fundamental usage patterns of TOPL, from basic placeholder syntax to common configuration scenarios you'll encounter in real projects.

## Placeholder Syntax

### Internal References

Use `${section.key}` to reference values within the same TOML file:

```toml
[server]
host = "localhost"
port = 8080
# Reference values from the same file
url = "http://${server.host}:${server.port}"

[database]
name = "myapp"
# Nested references work too
backup_name = "${database.name}_backup"
```

### External Parameters

Use `${parameter}` for values provided externally:

```toml
[api]
# These will be resolved from CLI parameters or function arguments
key = "${API_KEY}"
secret = "${API_SECRET}"
environment = "${ENV}"
```

### Mixed References

Combine internal and external references in the same value:

```toml
[app]
name = "myapp"
version = "1.0.0"

[deployment]
# Mix of internal reference and external parameter
image_tag = "${app.name}:${app.version}-${BUILD_NUMBER}"
# Result: "myapp:1.0.0-123" (if BUILD_NUMBER=123)
```

## File Organization

### Simple Structure

```toml
# config.toml
[app]
name = "MyApp"
debug = true

[database]
host = "localhost"
port = 5432
url = "postgresql://${database.host}:${database.port}/${DB_NAME}"
```

### Hierarchical Structure

```toml
# config.toml
[environments.development]
debug = true
db_host = "localhost"
api_url = "http://localhost:3000"

[environments.production]
debug = false
db_host = "prod-db.company.com"
api_url = "https://api.company.com"

[app]
# Reference nested values
debug_mode = "${environments.${ENVIRONMENT}.debug}"
database_host = "${environments.${ENVIRONMENT}.db_host}"
api_endpoint = "${environments.${ENVIRONMENT}.api_url}/v1"
```

## Command Line Usage

### Basic Command Structure

```bash
topl <config-file> [--parameter value] [--another-param value]
```

### Simple Example

```bash
# With a config file containing ${API_KEY} and ${DB_HOST}
topl app-config.toml --API_KEY "sk-abc123" --DB_HOST "localhost"
```

### Multiple Parameters

```bash
topl config.toml \
  --API_KEY "your-key" \
  --DB_HOST "localhost" \
  --DB_PORT "5432" \
  --ENVIRONMENT "development"
```

### Boolean and Numeric Parameters

```bash
# TOPL handles type conversion automatically
topl config.toml \
  --DEBUG "true" \
  --PORT "8080" \
  --TIMEOUT "30.5"
```

## Python API Usage

### Basic Resolution

```python
import tomllib
from topl import resolve_placeholders

# Load TOML file
with open('config.toml', 'rb') as f:
    data = tomllib.load(f)

# Resolve with external parameters
config = resolve_placeholders(
    data,
    API_KEY="your-secret-key",
    DB_HOST="localhost",
    ENVIRONMENT="development"
)

# Access resolved values
print(config.database.url)  # Fully resolved URL
print(config.api.key)       # "your-secret-key"
```

### Working with TOPLConfig Objects

```python
# TOPLConfig provides enhanced functionality
config = resolve_placeholders(data, **params)

# Check if all placeholders were resolved
if config.has_unresolved:
    print(f"Warning: {len(config.unresolved_placeholders)} unresolved placeholders")
    for placeholder in config.unresolved_placeholders:
        print(f"  - {placeholder}")

# Convert to plain dictionary if needed
plain_dict = config.to_dict()

# Access like a regular dictionary or with dot notation
database_url = config['database']['url']  # Dictionary style
database_url = config.database.url        # Dot notation style
```

### Error Handling

```python
from topl import resolve_placeholders
from topl.exceptions import CircularReferenceError

try:
    config = resolve_placeholders(data, **params)
except CircularReferenceError as e:
    print(f"Circular reference detected: {e}")
except Exception as e:
    print(f"Resolution failed: {e}")
```

## Common Patterns

### Environment-Based Configuration

```toml
# environments.toml
[defaults]
log_level = "INFO"
timeout = 30

[development]
debug = true
db_host = "localhost"
log_level = "DEBUG"

[production]
debug = false
db_host = "prod-server.com"
replicas = 3

[current]
# Select environment-specific values
debug = "${${ENVIRONMENT}.debug}"
database_host = "${${ENVIRONMENT}.db_host}"
log_level = "${${ENVIRONMENT}.log_level}"
```

Usage:
```bash
topl environments.toml --ENVIRONMENT "development"
topl environments.toml --ENVIRONMENT "production"
```

### Service Configuration Template

```toml
# services.toml
[common]
protocol = "https"
domain = "api.company.com"
version = "v2"
timeout = 30

[auth_service]
name = "authentication"
port = 8001
url = "${common.protocol}://${auth_service.name}.${common.domain}:${auth_service.port}/${common.version}"

[user_service]
name = "users"
port = 8002
url = "${common.protocol}://${user_service.name}.${common.domain}:${user_service.port}/${common.version}"
auth_url = "${auth_service.url}/verify"

[billing_service]
name = "billing"
port = 8003
url = "${common.protocol}://${billing_service.name}.${common.domain}:${billing_service.port}/${common.version}"
user_service_url = "${user_service.url}/user"
```

### Database Configuration

```toml
# database.toml
[connection]
driver = "postgresql"
host = "${DB_HOST}"
port = "${DB_PORT}"
database = "${DB_NAME}"
username = "${DB_USER}"
password = "${DB_PASSWORD}"

[urls]
# Build connection strings
primary = "${connection.driver}://${connection.username}:${connection.password}@${connection.host}:${connection.port}/${connection.database}"
readonly = "${connection.driver}://${connection.username}:${connection.password}@${connection.host}:${connection.port}/${connection.database}?options=-c%20default_transaction_isolation=serializable"

[pool]
min_connections = 5
max_connections = 20
timeout = "${connection.timeout}"
```

## Advanced Syntax Features

### Nested References

```toml
[level1]
value = "Hello"

[level2]
ref = "${level1.value}"

[level3]
# Reference a reference
nested_ref = "${level2.ref} World"
# Result: "Hello World"
```

### Array and Table References

```toml
[servers]
primary = "server1.com"
secondary = "server2.com"

[[services]]
name = "web"
host = "${servers.primary}"

[[services]]
name = "api" 
host = "${servers.secondary}"

[load_balancer]
# Reference array elements (this would need special handling)
upstream = "${servers.primary},${servers.secondary}"
```

### Conditional-Like Patterns

```toml
[app]
environment = "${ENVIRONMENT}"
debug = true

[logging]
# Simulate conditional logic
level = "${app.debug}"  # Will be "true" or "false"

[database]
# Different connection strings based on environment
host = "${${app.environment}_DB_HOST}"
# Requires: DEV_DB_HOST, PROD_DB_HOST, etc.
```

## Best Practices

### 1. Organize by Logical Groups

```toml
# Good: Logical grouping
[database]
host = "${DB_HOST}"
port = 5432

[api]  
key = "${API_KEY}"
url = "${API_URL}"

# Avoid: Flat structure for complex configs
api_key = "${API_KEY}"
api_url = "${API_URL}"
db_host = "${DB_HOST}"
```

### 2. Use Descriptive Parameter Names

```toml
# Good: Clear parameter names
database_url = "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

# Avoid: Ambiguous names
database_url = "postgresql://${U}:${P}@${H}:${PORT}/${DB}"
```

### 3. Provide Defaults Where Appropriate

```toml
[server]
host = "localhost"  # Default value
port = 8080         # Default value
# External parameter only when needed
ssl_cert = "${SSL_CERT_PATH}"
```

### 4. Document External Parameters

```toml
# Required external parameters:
# - API_KEY: Your service API key
# - ENVIRONMENT: deployment environment (dev/staging/prod)
# - DB_PASSWORD: Database password

[api]
key = "${API_KEY}"
environment = "${ENVIRONMENT}"

[database]
password = "${DB_PASSWORD}"
```

## Type Handling

TOPL preserves TOML data types during resolution:

```toml
[values]
# String
message = "Hello ${name}!"

# Integer  
port = 8080
timeout = "${TIMEOUT_SECONDS}"  # Will be converted to int if TIMEOUT_SECONDS="30"

# Float
rate = 1.5
multiplier = "${RATE_MULTIPLIER}"  # Will be float if RATE_MULTIPLIER="2.5"

# Boolean
debug = true
production = "${IS_PRODUCTION}"  # Will be boolean if IS_PRODUCTION="false"

# Arrays (placeholders in individual elements)
hosts = ["${PRIMARY_HOST}", "${SECONDARY_HOST}"]
```

## What's Next?

Now that you understand basic usage:

- **Deep dive into resolution** → [Chapter 4: Two-Phase Resolution System](04-two-phase-resolution.md)
- **Master the CLI** → [Chapter 5: CLI Reference](05-cli-reference.md)
- **See real examples** → [Chapter 7: Configuration & Examples](07-configuration-examples.md)

## Quick Reference

### Syntax Summary
```toml
# Internal reference
value = "${section.key}"

# External parameter  
value = "${PARAMETER}"

# Mixed
value = "${section.key}-${PARAMETER}"
```

### CLI Pattern
```bash
topl config.toml --PARAM1 value1 --PARAM2 value2
```

### Python API Pattern
```python
config = resolve_placeholders(data, PARAM1="value1", PARAM2="value2")
```