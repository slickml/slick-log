from importlib.metadata import distribution

import pytest
from assertpy import assert_that


def _get_valid_dependencies(dist_name: str = "slickcore") -> list[str]:
    """Helper function to retrieve the package dependencies names from `pyproject.toml`."""
    # map the libraries that their installation name differs from imported name (i.e. plugins)
    mapping = {
        "python-json-logger": "pythonjsonlogger",
    }
    deps = [dep.split(" ")[0] for dep in distribution(dist_name).requires]  # type: ignore
    return list({mapping[lib] if lib in mapping else lib for lib in deps})


def _get_invalid_dependencies() -> list[str]:
    """Helper function to return not-required / not-availabe dependencies cannot be imported."""
    return [
        "cookiecutter",
        "pyarrow",
        "plotly",
        "foo",
        "bar",
    ]


class TestImports:
    """Validates required and not-required dependencies imports."""

    @pytest.mark.parametrize(
        "package",
        _get_valid_dependencies(),
    )
    def test_imports__passes__with_valid_dependencies(self, package: str) -> None:
        """Validates all the required dependencies are imported successfully."""
        assert_that(__import__(package)).is_true()
        assert_that(__import__(package)).is_not_none()

    @pytest.mark.parametrize(
        "package",
        _get_invalid_dependencies(),
    )
    def test_imports__fails__with_invalid_dependencies(self, package: str) -> None:
        """Validates that not-required / not-availabe dependencies cannot be imported."""
        with pytest.raises(ModuleNotFoundError):
            __import__(package)
