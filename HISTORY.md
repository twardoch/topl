# The TOPL Chronicles: A Tale of Two-Phase Resolution
*A human-AI collaboration story*

## Genesis: When TOML Met Placeholders (July 23, 2025)

It all began with a deceptively simple README.md embedded inside itself—like a TOML Ouroboros. The project's origin story reads like something from a developer's fever dream: a **251-line Python script** masquerading as documentation, complete with shebang lines and dependency declarations tucked into a markdown file. 

```python
#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["python-box", "rich", "fire"]
# ///
```

The script promised something audacious: **two-phase placeholder resolution** for TOML files. Internal references first (`{{dict2.key2}}`), external parameters second (`{{external1}}`), warnings for the stubborn leftovers. It was elegant, minimal, and worked perfectly—but it was trapped in a README like a genie in a bottle.

### The Birth of Ambition

On July 23rd, 2025, at precisely 13:39:39 in Central European Time, Adam Twardoch made the fateful decision that would spawn this journey:

```
Initial commit
```

Three files. A `.gitignore` with 207 lines (because developers are paranoid), an MIT license, and a README.md with just two words: "# topl". The stage was set, but the script was still hiding in plain sight.

## The Great Transformation: Script to Package (July 23, 2025)

What happened next was nothing short of magical—the kind of human-AI pair programming that makes you believe in the future. In a single marathon session, the embedded script underwent a complete metamorphosis, transforming from a clever hack into a production-ready Python package.

### The Architecture Revolution

The transformation wasn't just about extracting code; it was about **reimagining the entire structure**:

```
topl/
├── src/topl/           # The heart of the operation
│   ├── core.py         # The two-phase resolution engine
│   ├── cli.py          # Fire-powered command interface
│   ├── utils.py        # The unsung heroes
│   ├── types.py        # Type safety's best friends
│   ├── exceptions.py   # When things go sideways
│   └── constants.py    # Magic numbers made respectable
└── tests/              # 44 tests and counting
    ├── unit/           # Testing the atoms
    └── integration/    # Testing the molecules
```

The original script's `_PLACEHOLDER_RE = re.compile(r"{{([^{}]+)}}")` became a proper constant in `constants.py`, while the humble `_get_by_path()` function graduated to `utils.py` with full type hints and error handling.

### The Two-Phase Philosophy

The core magic remained unchanged—that beautiful two-phase dance that makes TOPL special:

```python
# Phase 1: Internal Resolution - the introvert phase
for i in range(MAX_INTERNAL_PASSES):
    # Resolve {{section.key}} references within the file
    # Up to 10 passes to handle nested references
    # Break when nothing changes (stability achieved)

# Phase 2: External Resolution - the extrovert phase  
for key, parent in iter_box_strings(cfg):
    # Inject user-supplied parameters
    # {{param}} becomes the value you provided

# Phase 3: The Honesty Phase
# Warn about placeholders that couldn't be resolved
```

But now it lived in a proper `resolve_placeholders()` function with docstrings, type hints, and error handling that would make your mother proud.

### The TOPLConfig Revolution

Perhaps the most elegant addition was the `TOPLConfig` class—a Box wrapper that remembers its sins:

```python
class TOPLConfig:
    def __init__(self, data: Box, unresolved_placeholders: list[str] | None = None):
        self._data = data
        self._unresolved = unresolved_placeholders or []
        
    @property
    def has_unresolved(self) -> bool:
        return len(self._unresolved) > 0
```

It's like a configuration object with a conscience—it knows when it hasn't resolved everything and isn't afraid to tell you about it.

## The Testing Odyssey: 95% Coverage and Counting

The real proof of transformation came in the tests. What started as a simple script with embedded examples became a **44-test suite** covering every conceivable scenario:

- `test_basic_internal_resolution()` - Because the basics matter
- `test_circular_reference_detection()` - When placeholders chase their own tails
- `test_max_internal_passes_exceeded()` - When 10 isn't enough
- `test_unresolved_placeholder_tracking()` - Keeping tabs on the rebels

Each test told a story. The circular reference test, in particular, was a thing of beauty—watching the system gracefully detect when `{{a}}` referenced `{{b}}` which referenced `{{a}}` and throw a `CircularReferenceError` instead of hanging forever.

### The Modern Python Makeover

The transformation embraced everything that makes modern Python beautiful:

```python
# From humble beginnings...
def _get_by_path(box, dotted_path):
    # Classic Python, no hints, hope for the best

# To typed perfection...
def get_by_path(box: Box, dotted_path: str) -> Any:
    """Return value at dotted_path or None if invalid.
    
    Args:
        box: Box instance to search in
        dotted_path: Dot-separated path like "foo.bar.baz"
        
    Returns:
        Value at path or None if path doesn't exist
    """
```

Type hints everywhere. Docstrings with proper Args/Returns sections. Error handling that actually helps users instead of cryptic tracebacks.

## The Quality Revolution: When AIs Review Code (July 24, 2025)

Just when it seemed the package was complete, something fascinating happened—the code got reviewed by AI systems. Not just one, but multiple AI code reviewers with different specialties, each finding their own concerns and suggesting improvements.

### The Sourcery Suggestions

Sourcery AI, ever the pragmatist, focused on **memory efficiency**:
> "Why load the entire file into memory when you can stream it?"

This led to a elegant change in the CLI:

```python
# Before: Memory hog
with toml_path.open("rb") as f:
    data = f.read()
config = resolve_placeholders(tomllib.loads(data.decode()), **params)

# After: Stream-friendly  
with toml_path.open("rb") as f:
    config = resolve_placeholders(tomllib.load(f), **params)
```

### The Qodo Merge Pro Insights

Qodo Merge Pro played the paranoid security expert, worried about **input mutations**:
> "What if someone modifies the original data during resolution?"

This sparked the addition of deep copying to protect the original data:

```python
import copy
cfg = Box(copy.deepcopy(data), default_box=True, default_box_attr=None)
```

### The List Revolution

But the most interesting suggestion was extending placeholder resolution to **lists and sequences**:

```python
# Now this works:
values = ["{{base}}-1", "{{base}}-2", "{{base}}-3"]
# With base = "server", becomes:
# ["server-1", "server-2", "server-3"]
```

The `iter_box_strings()` function grew a nested helper:

```python
def _iter_container(container: Sequence[Any], parent: Box, parent_key: str) -> None:
    """Handle lists, tuples, and other sequences."""
    for i, item in enumerate(container):
        if isinstance(item, str):
            results.append((i, parent[parent_key]))  # Clever indexing trick
```

## The Documentation Dynasty (August 2025)

As the package matured, it developed an impressive documentation ecosystem:

- **CLAUDE.md** - The AI whisperer's guide to working with the codebase
- **WORK.md** - Real-time development diary with brutal honesty about what's broken
- **TODO.md** - The master plan, 261 items strong
- **CHANGELOG.md** - Because we're professionals here

The `src_docs/` directory bloomed with MkDocs-powered documentation, complete with:
- Getting Started guides
- API references with real examples
- Troubleshooting guides (because users will find ways to break anything)

## The Version Dance: v1.0.0 to v1.0.5 in One Day

July 24th, 2025 was a day of rapid-fire releases. Version tags flew like confetti:
- `v1.0.0` - "We did it!"
- `v1.0.1` - "Wait, we forgot something..."
- `v1.0.2` - "Okay, now we got it..."
- `v1.0.3` - "Third time's the charm?"
- `v1.0.4` - "Seriously, this time..."
- `v1.0.5` - "Finally stable!"

Each version incorporated feedback and fixes, the hallmark of iterative development at its finest.

## The CI/CD Chronicles: Automation Station

The package didn't just get code—it got a **full GitHub Actions workflow suite**:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
        os: [ubuntu-latest, windows-latest, macos-latest]
```

Because if you're going to do it, do it across 9 different environments simultaneously.

The release workflow was particularly elegant, featuring:
- Automatic PyPI publishing on git tags
- Test PyPI for safety testing
- Dependabot keeping dependencies fresh
- Security scanning with Bandit

## The Philosophy of Two-Phase Resolution

Throughout this journey, the core philosophy remained unchanged—the beauty of **two-phase resolution**:

1. **Be introspective first** - Resolve what you can from within
2. **Accept help from outside** - But only after you've helped yourself  
3. **Be honest about limitations** - Warn about what you can't resolve

This mirrors good software design principles: self-sufficiency, clear interfaces, and transparent error handling.

## The Human-AI Collaboration Magic

What makes this story special isn't just the technical achievement—it's the **collaboration pattern** that emerged:

- **Human vision**: Adam provided the original script and the ambition to transform it
- **AI execution**: Claude handled the systematic transformation, testing, and documentation
- **AI feedback**: Multiple AI reviewers provided different perspectives and caught edge cases
- **Iterative refinement**: Each suggestion led to better code and more robust functionality

The commit messages tell the story:

```
🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

Every commit was a true collaboration—human creativity and AI systematic thoroughness working in harmony.

## The Legacy: From Script to Package

Today, TOPL stands as a testament to what's possible when you combine:
- A clever idea (two-phase resolution)
- Modern Python practices (type hints, proper packaging)  
- Comprehensive testing (95% coverage)
- AI-assisted development (systematic and thorough)
- Real-world feedback (AI code reviews)

The original 251-line script embedded in a README has become a **production-ready package** with:
- 🔢 **1,200+ lines** of well-structured code
- 🧪 **44 comprehensive tests** covering edge cases
- 📚 **Complete documentation** with examples
- 🚀 **Modern CI/CD pipeline** with multi-platform testing
- 🎯 **Zero regression** from the original functionality

## The Future: Phase 2 and Beyond

As this history is written, TOPL enters Phase 2 with ambitious goals:
- Performance benchmarking
- Advanced CLI features (dry-run, validation modes)
- Async support for large files
- Plugin system for custom resolvers

The TODO.md file lists 261 items across three phases, a roadmap that would make any project manager weep with joy (or terror).

## Epilogue: Lessons in Collaboration

The TOPL story demonstrates that the future of software development isn't human vs. AI—it's human **with** AI. The combination of human creativity, vision, and domain expertise with AI's systematic thoroughness, attention to detail, and rapid iteration creates something neither could achieve alone.

From a simple script hiding in a README to a production-ready Python package in just over a month—that's the power of collaboration in the age of AI.

*May your placeholders always resolve, and may your two phases never become three.*

---

*This history was written in collaboration between human and AI, continuing the project's tradition of partnership. The story will continue as TOPL evolves through its planned phases of development.*