"""Type definitions for the topl package.

# this_file: src/topl/types.py
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

# Type aliases for better readability
TOMLData = dict[str, Any]
ConfigMapping = Mapping[str, Any]
PlaceholderParams = dict[str, str]
NestedValue = str | dict[str, Any] | Any
