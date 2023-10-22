"""Tests for Jack-of-All-Templates Julia specific build."""

from __future__ import annotations

from pathlib import Path

import copier
import pytest

PROJECT_ROOT = Path(__file__).parent.parent


def test_julia_fully_templated(
    tmp_path: Path, julia_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / julia_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=julia_base_answers,
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


def test_julia_constant_file_content(
    tmp_path: Path, julia_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / julia_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=julia_base_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    project_name = julia_base_answers["project_name"]
    readme_path = dst_path / "README.rst"
    project_path = dst_path / "Project.toml"
    module_path = dst_path / "src" / f"{julia_base_answers['julia_module_name']}.jl"

    helpers.assert_file_content(readme_path, [f"{project_name}\n====================="])
    helpers.assert_file_content(
        project_path,
        [
            f"name = \"{julia_base_answers['julia_module_name']}\"",
            f"uuid = \"{julia_base_answers['julia_project_uuid']}\"",
        ],
    )

    assert module_path.exists()


@pytest.mark.parametrize(("include_docs"), [True, False])
def test_julia_docs(
    tmp_path: Path, julia_base_answers: dict[str, str | bool], helpers, include_docs
):
    dst_path = tmp_path / julia_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**julia_base_answers, "julia_include_docs": include_docs},
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    project_name = julia_base_answers["project_name"]
    repository_namespace = julia_base_answers["repository_namespace"]
    docs_path = dst_path / "docs"
    readme_path = dst_path / "README.rst"

    if not include_docs:
        assert not docs_path.exists()
        helpers.assert_file_content(
            readme_path,
            unexpected_strs=[
                f"Documentation: https://{repository_namespace}.codeberg.org/{project_name}/stable/",
                "|juliadoc-shield|",
            ],
        )
    else:
        assert docs_path.exists()
        helpers.assert_file_content(
            readme_path,
            [
                f"Documentation: https://{repository_namespace}.codeberg.org/{project_name}/stable/",
                "|juliadoc-shield|",
            ],
        )
