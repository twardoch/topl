# Chapter 6: API Reference

Complete Python API documentation for programmatic usage of TOPL in your applications.

## Core Functions

### `resolve_placeholders()`

The main function for resolving placeholders in TOML data.

```python
def resolve_placeholders(data: ConfigMapping, **params: str) -> TOPLConfig:
    """Resolve placeholders inside data and return a TOPLConfig instance.
    
    Args:
        data: Mapping returned by tomllib.load or similar
        **params: External parameters used during the external phase
        
    Returns:
        TOPLConfig instance with resolved data and metadata
        
    Raises:
        CircularReferenceError: If circular references are detected
    """
```

#### Parameters

- **`data`** (`dict[str, Any]`): TOML data structure, typically from `tomllib.load()`
- **`**params`** (`str`): External parameters as keyword arguments

#### Returns

Returns a `TOPLConfig` instance containing:
- Resolved configuration data
- List of unresolved placeholders
- Metadata about the resolution process

#### Examples

```python
import tomllib
from topl import resolve_placeholders

# Basic usage
with open('config.toml', 'rb') as f:
    data = tomllib.load(f)
    
config = resolve_placeholders(data, API_KEY="secret", DEBUG="true")
print(config.api.key)  # "secret"
```

```python
# Handle unresolved placeholders
config = resolve_placeholders(data, PARTIAL_PARAM="value")

if config.has_unresolved:
    print(f"Warning: {len(config.unresolved_placeholders)} unresolved")
    for placeholder in config.unresolved_placeholders:
        print(f"  {placeholder}")
```

## Classes

### `TOPLConfig`

Wrapper class for resolved configuration data with enhanced functionality.

```python
class TOPLConfig:
    """Wrapper for resolved TOML configuration with placeholder metadata."""
```

#### Properties

##### `data` → `Box`

Access the underlying Box data structure.

```python
config = resolve_placeholders(data, **params)
box_data = config.data
print(type(box_data))  # <class 'box.Box'>
```

##### `unresolved_placeholders` → `list[str]`

List of placeholders that couldn't be resolved.

```python
config = resolve_placeholders(data)
if config.unresolved_placeholders:
    print("These placeholders need values:")
    for placeholder in config.unresolved_placeholders:
        print(f"  {placeholder}")
```

##### `has_unresolved` → `bool`

Check if there are any unresolved placeholders.

```python
config = resolve_placeholders(data, **params)
if config.has_unresolved:
    print("Some placeholders remain unresolved")
    # Handle missing parameters
```

#### Methods

##### `to_dict()` → `dict[str, Any]`

Convert to plain Python dictionary.

```python
config = resolve_placeholders(data, **params)
plain_dict = config.to_dict()

# Use with libraries that expect plain dicts
import json
json.dump(plain_dict, output_file)
```

##### `__getattr__(name)` → `Any`

Delegate attribute access to underlying Box.

```python
config = resolve_placeholders(data, **params)

# These are equivalent:
value1 = config.database.host
value2 = config.data.database.host
```

##### `__getitem__(key)` → `Any`

Delegate dictionary-style access to underlying Box.

```python
config = resolve_placeholders(data, **params)

# Dictionary-style access
db_config = config['database']
host = config['database']['host']

# Mixed access styles
host = config['database'].host
```

## Utility Functions

### `get_by_path()`

Get value from Box using dotted path notation.

```python
def get_by_path(box: Box, dotted_path: str) -> Any:
    """Return value at dotted_path or None if path is invalid."""
```

```python
from topl.utils import get_by_path
from box import Box

data = Box({"app": {"database": {"host": "localhost"}}})
host = get_by_path(data, "app.database.host")  # "localhost"
missing = get_by_path(data, "app.missing.key")  # None
```

### `iter_box_strings()`

Iterate over all string values in a Box structure.

```python
def iter_box_strings(box: Box) -> Generator[tuple[str | int, Any], None, None]:
    """Yield (key, parent_container) pairs for every string leaf."""
```

```python
from topl.utils import iter_box_strings
from box import Box

data = Box({
    "name": "app",
    "config": {"debug": "true", "host": "localhost"},
    "tags": ["web", "api"]
})

for key, parent in iter_box_strings(data):
    print(f"Found string at {key}: {parent[key]}")
# Output:
# Found string at name: app
# Found string at debug: true  
# Found string at host: localhost
# Found string at 0: web
# Found string at 1: api
```

## Exception Classes

### `CircularReferenceError`

Raised when circular placeholder references are detected.

```python
from topl.exceptions import CircularReferenceError

try:
    config = resolve_placeholders(data_with_circular_refs)
except CircularReferenceError as e:
    print(f"Circular reference: {e}")
    # Handle the error appropriately
```

### `PlaceholderResolutionError`

Base exception for placeholder resolution issues.

```python
from topl.exceptions import PlaceholderResolutionError

try:
    config = resolve_placeholders(data, **params)
except PlaceholderResolutionError as e:
    print(f"Resolution failed: {e}")
```

### `InvalidTOMLError`

Raised when TOML parsing fails.

```python
from topl.exceptions import InvalidTOMLError

try:
    with open('invalid.toml', 'rb') as f:
        data = tomllib.load(f)
except InvalidTOMLError as e:
    print(f"Invalid TOML: {e}")
```

### `FileNotFoundError`

TOPL-specific file not found error.

```python
from topl.exceptions import FileNotFoundError as TOPLFileNotFoundError

try:
    config = load_toml_file(Path("missing.toml"))
except TOPLFileNotFoundError as e:
    print(f"File not found: {e}")
```

## Type Hints

### Core Types

```python
from typing import Any, Mapping
from topl.types import ConfigMapping, PlaceholderParams

# Type aliases used throughout the API
ConfigMapping = Mapping[str, Any]          # Input configuration data
PlaceholderParams = Mapping[str, str]      # External parameters
```

### Function Signatures

```python
# Complete function signatures with types
def resolve_placeholders(
    data: ConfigMapping, 
    **params: str
) -> TOPLConfig: ...

def get_by_path(
    box: Box, 
    dotted_path: str
) -> Any: ...

def iter_box_strings(
    box: Box
) -> Generator[tuple[str | int, Any], None, None]: ...
```

## CLI Integration

### `main_cli()`

Main CLI function that can be called programmatically.

```python
def main_cli(path: str, verbose: bool = False, **params: str) -> None:
    """Main CLI function for processing TOML files."""
```

```python
from topl.cli import main_cli

# Call CLI function directly
main_cli("config.toml", verbose=True, API_KEY="secret", DEBUG="true")
```

### `load_toml_file()`

Load and parse TOML files with proper error handling.

```python
def load_toml_file(path: Path) -> dict[str, Any]:
    """Load and parse a TOML file with error handling."""
```

```python
from pathlib import Path
from topl.cli import load_toml_file

data = load_toml_file(Path("config.toml"))
config = resolve_placeholders(data, **params)
```

## Integration Patterns

### With Web Frameworks

#### Flask Integration

```python
from flask import Flask
from topl import resolve_placeholders
import tomllib

app = Flask(__name__)

# Load configuration at startup
with open('config.toml', 'rb') as f:
    toml_data = tomllib.load(f)

config = resolve_placeholders(
    toml_data,
    DB_PASSWORD=os.environ['DB_PASSWORD'],
    SECRET_KEY=os.environ['SECRET_KEY']
)

app.config.update(config.to_dict())
```

#### Django Integration

```python
# settings.py
import os
from pathlib import Path
from topl import resolve_placeholders
import tomllib

BASE_DIR = Path(__file__).resolve().parent.parent

# Load TOPL configuration
config_file = BASE_DIR / 'config.toml'
with config_file.open('rb') as f:
    toml_data = tomllib.load(f)

topl_config = resolve_placeholders(
    toml_data,
    SECRET_KEY=os.environ['SECRET_KEY'],
    DB_PASSWORD=os.environ['DB_PASSWORD'],
    DEBUG=os.environ.get('DEBUG', 'false')
)

# Use resolved configuration
SECRET_KEY = topl_config.django.secret_key
DEBUG = topl_config.django.debug
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': topl_config.database.name,
        'USER': topl_config.database.user,
        'PASSWORD': topl_config.database.password,
        'HOST': topl_config.database.host,
        'PORT': topl_config.database.port,
    }
}
```

### With Configuration Management

#### Pydantic Models

```python
from pydantic import BaseModel
from topl import resolve_placeholders
import tomllib

class DatabaseConfig(BaseModel):
    host: str
    port: int
    name: str
    url: str

class AppConfig(BaseModel):
    name: str
    debug: bool
    database: DatabaseConfig

# Load and validate with Pydantic
with open('config.toml', 'rb') as f:
    data = tomllib.load(f)

resolved = resolve_placeholders(data, **os.environ)
config = AppConfig(**resolved.to_dict())
```

#### Dataclasses

```python
from dataclasses import dataclass
from topl import resolve_placeholders

@dataclass
class Config:
    api_key: str
    db_host: str
    debug: bool
    
    @classmethod
    def from_toml(cls, file_path: str, **params: str) -> 'Config':
        with open(file_path, 'rb') as f:
            data = tomllib.load(f)
        
        resolved = resolve_placeholders(data, **params)
        return cls(
            api_key=resolved.api.key,
            db_host=resolved.database.host,
            debug=resolved.app.debug
        )

# Usage
config = Config.from_toml('app.toml', API_KEY=api_key, DB_HOST=db_host)
```

### With Async Code

```python
import asyncio
from topl import resolve_placeholders

async def load_config() -> TOPLConfig:
    """Async configuration loading."""
    # Load TOML data (sync operation)
    with open('config.toml', 'rb') as f:
        data = tomllib.load(f)
    
    # Get parameters from async sources
    api_key = await get_secret('api-key')
    db_password = await get_secret('db-password')
    
    return resolve_placeholders(
        data,
        API_KEY=api_key,
        DB_PASSWORD=db_password
    )

async def main():
    config = await load_config()
    print(f"Database URL: {config.database.url}")

asyncio.run(main())
```

## Performance Considerations

### Memory Usage

```python
import tracemalloc
from topl import resolve_placeholders

# Monitor memory usage
tracemalloc.start()

config = resolve_placeholders(large_config_data, **params)

current, peak = tracemalloc.get_traced_memory()
print(f"Memory usage: {current / 1024 / 1024:.1f}MB (peak: {peak / 1024 / 1024:.1f}MB)")
tracemalloc.stop()
```

### Caching Results

```python
from functools import lru_cache
from topl import resolve_placeholders

@lru_cache(maxsize=128)
def get_resolved_config(config_hash: str, **params: str) -> TOPLConfig:
    """Cache resolved configurations."""
    with open('config.toml', 'rb') as f:
        data = tomllib.load(f)
    return resolve_placeholders(data, **params)

# Usage with stable parameters
config = get_resolved_config("v1", API_KEY=api_key, ENV=environment)
```

## What's Next?

- **See real-world examples** → [Chapter 7: Configuration & Examples](07-configuration-examples.md)
- **Troubleshoot issues** → [Chapter 8: Troubleshooting](08-troubleshooting.md)
- **Contribute to development** → [Chapter 9: Development & Contributing](09-development-contributing.md)

## Quick Reference

### Essential Imports
```python
import tomllib
from topl import resolve_placeholders
from topl.exceptions import CircularReferenceError
```

### Basic Pattern
```python
# Load → Resolve → Use
with open('config.toml', 'rb') as f:
    data = tomllib.load(f)

config = resolve_placeholders(data, **params)
value = config.section.key
```

### Error Handling
```python
try:
    config = resolve_placeholders(data, **params)
except CircularReferenceError:
    # Handle circular references
    pass
```