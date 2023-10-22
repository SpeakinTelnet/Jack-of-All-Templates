"""Tests for Jack-of-All-Templates Solidity specific build."""

from __future__ import annotations

from pathlib import Path

import copier

PROJECT_ROOT = Path(__file__).parent.parent


def test_solidity_fully_templated(
    tmp_path: Path, solidity_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / solidity_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=solidity_base_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    helpers.detect_unprocessed_jinja(
        dst_path,
        [
            dst_path / ".gitea",
        ],
    )


def test_solidity_constant_file_content(
    tmp_path: Path, solidity_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / solidity_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=solidity_base_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    project_name = solidity_base_answers["project_name"]
    readme_path = dst_path / "README.rst"
    pyproject_path = dst_path / "pyproject.toml"

    helpers.assert_file_content(readme_path, [f"{project_name}\n====================="])
    helpers.assert_file_content(
        pyproject_path,
        [f"name = \"{project_name.replace(' ', '_')}\""],
    )
