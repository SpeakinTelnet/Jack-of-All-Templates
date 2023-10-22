"""Configuration module for the tests."""

from pathlib import Path
from typing import Sequence

import pytest


class Helpers:
    """Reusable functions for testing."""

    @classmethod
    def detect_unprocessed_jinja(
        cls,
        top_path: Path,
        ignored_subfolder: Sequence[Path] = (),
    ) -> None:
        """Walk the top path recursively to check for unprocessed jinja template."""
        for p in Path(top_path).iterdir():
            for symbols in ["{%", "%}", "{{", "}}"]:
                assert symbols not in p.name

            if p.is_dir():
                if p not in ignored_subfolder:
                    cls.detect_unprocessed_jinja(p)
                continue
            try:
                file_content = p.read_text()
            except UnicodeDecodeError:  # catch for non text files (i.e: .png, .jpg)
                continue
            for symbols in ["{%", "%}", "{{", "}}"]:
                assert symbols not in file_content

    @staticmethod
    def assert_file_content(
        file_path: Path,
        expected_strs: Sequence[str] = (),
        unexpected_strs: Sequence[str] = (),
    ) -> None:
        """Check the provided file's content for expected and unexpected strings."""
        assert file_path.exists()
        file_content = file_path.read_text()
        for content in expected_strs:
            assert content in file_content
        for content in unexpected_strs:
            assert content not in file_content


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture
def python_base_answers():
    return {
        "project_language": "Python",
        "project_name": "python-test",
        "project_description": "Python test description",
        "author_name": "SpeakinTelnet",
        "author_email": "SpeakinTelnet@example.com",
        "repository_provider": "codeberg.org",
        "repository_namespace": "python-test",
        "repo_url": "https://www.codeberg.org/SpeakinTelnet/python-test",
        "license_date": "2023",
        "python_include_docs": True,
        "python_include_brownie": True,
        "python_module_name": "python_test",
    }


@pytest.fixture
def julia_base_answers():
    return {
        "project_language": "Julia",
        "project_name": "julia-test",
        "project_description": "Julia test description",
        "author_name": "SpeakinTelnet",
        "author_email": "SpeakinTelnet@example.com",
        "repository_provider": "codeberg.org",
        "repository_namespace": "python-test",
        "repo_url": "https://www.codeberg.org/SpeakinTelnet/julia-test",
        "license_date": "2023",
        "julia_include_docs": True,
        "julia_module_name": "julia_test",
        "julia_project_uuid": "bbfa0e73-1458-65bf-d411-d779008015e5",
    }


@pytest.fixture
def rust_base_answers():
    return {
        "project_language": "Rust",
        "project_name": "rust-test",
        "project_description": "Rust test description",
        "author_name": "SpeakinTelnet",
        "author_email": "SpeakinTelnet@example.com",
        "repository_provider": "codeberg.org",
        "repository_namespace": "rust-test",
        "repo_url": "https://www.codeberg.org/SpeakinTelnet/rust-test",
        "license_date": "2023",
        "rust_targets": "Other",
        "rust_include_examples": True,
        "rust_include_benchmark": True,
    }


@pytest.fixture
def solidity_base_answers():
    return {
        "project_language": "Solidity",
        "project_name": "solidity-test",
        "project_description": "Solidity test description",
        "author_name": "SpeakinTelnet",
        "author_email": "SpeakinTelnet@example.com",
        "repository_provider": "codeberg.org",
        "repository_namespace": "solidity-test",
        "repo_url": "https://www.codeberg.org/SpeakinTelnet/solidity-test",
        "license_date": "2023",
    }
