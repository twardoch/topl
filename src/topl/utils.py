"""Utility functions for placeholder resolution.

# this_file: src/topl/utils.py
"""

from __future__ import annotations

import re
from collections.abc import Generator, Mapping
from typing import Any

from box import Box

from .constants import PLACEHOLDER_PATTERN
from .types import PlaceholderParams


def get_by_path(box: Box, dotted_path: str) -> Any:
    """Return value at dotted_path or None if the path is invalid.

    Args:
        box: Box instance to search in
        dotted_path: Dot-separated path like "foo.bar.baz"

    Returns:
        Value at the specified path, or None if path doesn't exist

    Examples:
        >>> data = Box({"a": {"b": {"c": "value"}}})
        >>> get_by_path(data, "a.b.c")
        'value'
        >>> get_by_path(data, "a.missing")
        None
    """
    current = box
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def resolve_internal_once(s: str, root: Box) -> str:
    """Replace one pass of internal placeholders in string s.

    A placeholder is internal if the path exists in root.

    Args:
        s: String potentially containing placeholders
        root: Root Box instance to resolve against

    Returns:
        String with internal placeholders resolved

    Examples:
        >>> data = Box({"name": "world"})
        >>> resolve_internal_once("Hello {{name}}!", data)
        'Hello world!'
    """

    def repl(match: re.Match[str]) -> str:
        path = match.group(1).strip()
        value = get_by_path(root, path)
        return str(value) if value is not None else match.group(0)

    return PLACEHOLDER_PATTERN.sub(repl, s)


def resolve_external(s: str, params: PlaceholderParams) -> str:
    """Replace external placeholders using string formatting.

    We temporarily convert {{name}} → {name} then format.
    Missing keys are left untouched.

    Args:
        s: String potentially containing placeholders
        params: External parameters for substitution

    Returns:
        String with external placeholders resolved

    Examples:
        >>> resolve_external("Hello {{name}}!", {"name": "world"})
        'Hello world!'
        >>> resolve_external("Hello {{missing}}!", {})
        'Hello {{missing}}!'
    """

    class SafeDict(dict):
        """Dict that leaves unknown placeholders unchanged."""

        def __missing__(self, key: str) -> str:
            return f"{{{{{key}}}}}"

    if not params:
        return s

    # Convert {{name}} → {name}
    tmp = PLACEHOLDER_PATTERN.sub(lambda m: "{" + m.group(1).strip() + "}", s)
    return tmp.format_map(SafeDict(params))


def iter_box_strings(box: Box) -> Generator[tuple[str, Box], None, None]:
    """Yield (key, parent_box) pairs for every string leaf in box.

    We return both key and the parent so we can assign new values in-place.

    Args:
        box: Box instance to iterate through

    Yields:
        Tuple of (key, parent_box) for each string value found

    Examples:
        >>> data = Box({"a": "text", "b": {"c": "more text"}})
        >>> list(iter_box_strings(data))
        [('a', Box(...)), ('c', Box(...))]
    """
    for key, val in box.items():
        if isinstance(val, str):
            yield key, box
        elif isinstance(val, Mapping):
            yield from iter_box_strings(val)  # type: ignore[arg-type]
