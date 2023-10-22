"""Tests for Jack-of-All-Templates Python specific build."""

from __future__ import annotations

from pathlib import Path

import copier
import pytest

PROJECT_ROOT = Path(__file__).parent.parent


def test_python_fully_templated(
    tmp_path: Path, python_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / python_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=python_base_answers,
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


def test_python_constant_file_content(
    tmp_path: Path, python_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / python_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=python_base_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    project_name = python_base_answers["project_name"]
    readme_path = dst_path / "README.rst"
    pyproject_path = dst_path / "pyproject.toml"
    module_path = dst_path / "src" / python_base_answers["python_module_name"]

    helpers.assert_file_content(readme_path, [f"{project_name}\n====================="])
    helpers.assert_file_content(
        pyproject_path,
        [f"name = \"{project_name.replace(' ', '_')}\""],
    )

    assert module_path.exists()


@pytest.mark.parametrize(("include_docs"), [True, False])
def test_python_docs(
    tmp_path: Path, python_base_answers: dict[str, str | bool], helpers, include_docs
):
    dst_path = tmp_path / python_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**python_base_answers, "python_include_docs": include_docs},
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    project_name = python_base_answers["project_name"]
    docs_path = dst_path / "docs"
    readme_path = dst_path / "README.rst"
    pyproject_path = dst_path / "pyproject.toml"
    index_path = dst_path / "docs" / "index.rst"
    conf_path = dst_path / "docs" / "conf.py"

    if not include_docs:
        assert not docs_path.exists()
        helpers.assert_file_content(
            readme_path,
            unexpected_strs=[
                f"Documentation: https://{project_name}.readthedocs.io",
                "|readthedocs_shield|",
            ],
        )
        helpers.assert_file_content(
            pyproject_path,
            unexpected_strs=[
                "[tool.hatch.envs.docs]",
            ],
        )
    else:
        assert docs_path.exists()
        helpers.assert_file_content(
            index_path,
            [
                f"Welcome to {project_name}'s documentation!",
                python_base_answers["project_description"],
            ],
        )
        helpers.assert_file_content(
            conf_path,
            [f"import {python_base_answers['python_module_name']}"],
        )


@pytest.mark.parametrize(("include_brownie"), [True, False])
def test_python_brownie(
    tmp_path: Path, python_base_answers: dict[str, str | bool], helpers, include_brownie
):
    dst_path = tmp_path / python_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**python_base_answers, "python_include_brownie": include_brownie},
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    build_path = dst_path / "build"
    contracts_path = dst_path / "contracts"
    interfaces_path = dst_path / "interfaces"
    reports_path = dst_path / "reports"
    scripts_path = dst_path / "scripts"
    brownie_conf = dst_path / "brownie-config.yaml"
    pyproject_path = dst_path / "pyproject.toml"

    if not include_brownie:
        assert not build_path.exists()
        assert not contracts_path.exists()
        assert not interfaces_path.exists()
        assert not reports_path.exists()
        assert not scripts_path.exists()
        assert not brownie_conf.exists()

        helpers.assert_file_content(
            pyproject_path,
            [
                '"pytest >= 7.0",',
            ],
            ['"pytest >= 6.2.5",', '"eth-brownie >= 1.19",'],
        )
    else:
        assert build_path.exists()
        assert contracts_path.exists()
        assert interfaces_path.exists()
        assert reports_path.exists()
        assert scripts_path.exists()
        assert brownie_conf.exists()

        helpers.assert_file_content(
            pyproject_path,
            ['"pytest >= 6.2.5",', '"eth-brownie >= 1.19",'],
            [
                '"pytest >= 7.0",',
            ],
        )
