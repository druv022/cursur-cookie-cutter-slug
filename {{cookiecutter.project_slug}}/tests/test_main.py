"""Tests for main module."""
{% if cookiecutter.testing_framework == 'pytest' %}

from typing import TYPE_CHECKING

import pytest

from {{ cookiecutter.project_slug }} import __version__

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture


def test_version() -> None:
    """Test that version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_import() -> None:
    """Test that the package can be imported."""
    from {{ cookiecutter.project_slug }} import main as main_module

    assert main_module is not None


def test_main_function_execution(capsys: "CaptureFixture[str]") -> None:
    """Test that main function executes without errors."""
    from {{ cookiecutter.project_slug }}.main import main

    main()
    captured = capsys.readouterr()
    assert isinstance(captured.out, str)
    assert callable(main)


def test_main_function_import() -> None:
    """Test that main function can be imported and called."""
    from {{ cookiecutter.project_slug }}.main import main

    # Verify function exists and is callable
    assert callable(main)

    # Call function and verify no exceptions
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() raised {e} unexpectedly")
{% else %}

import unittest

from {{ cookiecutter.project_slug }} import __version__


class TestVersion(unittest.TestCase):
    """Tests for package version."""

    def test_version_is_defined(self) -> None:
        """Test that version is defined."""
        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)


class TestImport(unittest.TestCase):
    """Tests for package import."""

    def test_main_module_can_be_imported(self) -> None:
        """Test that the package can be imported."""
        from {{ cookiecutter.project_slug }} import main

        self.assertIsNotNone(main)

    def test_main_function_is_callable(self) -> None:
        """Test that main function can be imported and called."""
        from {{ cookiecutter.project_slug }}.main import main

        self.assertTrue(callable(main))

    def test_main_function_executes_without_error(self) -> None:
        """Test that main function executes without errors."""
        from {{ cookiecutter.project_slug }}.main import main

        try:
            main()
        except Exception as e:
            self.fail(f"main() raised {e} unexpectedly")


if __name__ == "__main__":
    unittest.main()
{% endif %}
