"""Unit tests for core functionality.

# this_file: tests/unit/test_core.py
"""

from __future__ import annotations

import pytest

from topl import CircularReferenceError, resolve_placeholders


class TestResolvePlaceholders:
    """Tests for the resolve_placeholders function."""

    def test_simple_internal_resolution(self, sample_toml_data):
        """Test basic internal placeholder resolution."""
        config = resolve_placeholders(sample_toml_data)
        assert config.greeting == "Hello world!"
        assert config.nested.message == "This is test"

    def test_external_parameters(self, external_placeholder_data):
        """Test external parameter resolution."""
        config = resolve_placeholders(
            external_placeholder_data,
            external_name="Alice",
            user="john",
            project="myapp",
        )
        assert config.message == "Hello Alice!"
        assert config.path == "/home/john/myapp"

    def test_mixed_resolution(self, mixed_placeholder_data):
        """Test mixed internal and external resolution."""
        config = resolve_placeholders(mixed_placeholder_data, environment="prod")
        assert config.full_name == "myapp-1.0.0"
        assert config.deployment_path == "/opt/prod/myapp-1.0.0"

    def test_circular_reference_detection(self):
        """Test detection of circular references."""
        # Create a scenario that will actually trigger maximum passes
        # by creating deeply nested references that keep expanding
        circular_data = {
            "base": "{{level1}}",
            "level1": "{{level2}}-suffix1",
            "level2": "{{level3}}-suffix2",
            "level3": "{{level4}}-suffix3",
            "level4": "{{level5}}-suffix4",
            "level5": "{{level6}}-suffix5",
            "level6": "{{level7}}-suffix6",
            "level7": "{{level8}}-suffix7",
            "level8": "{{level9}}-suffix8",
            "level9": "{{level10}}-suffix9",
            "level10": "{{level11}}-suffix10",
            "level11": "{{base}}-suffix11",  # This creates the cycle
        }

        with pytest.raises(CircularReferenceError):
            resolve_placeholders(circular_data)

    def test_unresolved_placeholders(self):
        """Test handling of unresolved placeholders."""
        data = {"message": "Hello {{missing}}!"}
        config = resolve_placeholders(data)

        assert config.has_unresolved
        assert "{{missing}}" in config.unresolved_placeholders
        assert config.message == "Hello {{missing}}!"

    def test_no_placeholders(self):
        """Test data without any placeholders."""
        data = {"simple": "value", "number": 42}
        config = resolve_placeholders(data)

        assert not config.has_unresolved
        assert config.simple == "value"
        assert config.number == 42


class TestTOPLConfig:
    """Tests for the TOPLConfig wrapper class."""

    def test_config_creation(self, sample_toml_data):
        """Test basic config creation and access."""
        config = resolve_placeholders(sample_toml_data)

        # Test attribute access
        assert config.name == "world"
        assert config.greeting == "Hello world!"

        # Test item access
        assert config["name"] == "world"
        assert config["greeting"] == "Hello world!"

    def test_to_dict_conversion(self, sample_toml_data):
        """Test conversion to plain dictionary."""
        config = resolve_placeholders(sample_toml_data)
        result_dict = config.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["name"] == "world"
        assert result_dict["greeting"] == "Hello world!"

    def test_unresolved_tracking(self):
        """Test tracking of unresolved placeholders."""
        data = {"resolved": "Hello {{name}}!", "unresolved": "Missing {{missing}}!"}
        config = resolve_placeholders(data, name="world")

        assert config.resolved == "Hello world!"
        assert config.unresolved == "Missing {{missing}}!"
        assert config.has_unresolved
        assert len(config.unresolved_placeholders) == 1
        assert "{{missing}}" in config.unresolved_placeholders

    def test_repr_with_unresolved(self):
        """Test string representation with unresolved placeholders."""
        data = {"message": "Hello {{missing}}!"}
        config = resolve_placeholders(data)
        repr_str = repr(config)

        assert "TOPLConfig" in repr_str
        assert "1 unresolved" in repr_str

    def test_repr_without_unresolved(self, sample_toml_data):
        """Test string representation without unresolved placeholders."""
        config = resolve_placeholders(sample_toml_data)
        repr_str = repr(config)

        assert "TOPLConfig" in repr_str
        assert "unresolved" not in repr_str
