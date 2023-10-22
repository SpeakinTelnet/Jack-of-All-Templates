"""Tests for Jack-of-All-Templates Rust specific build."""

from __future__ import annotations

from pathlib import Path

import copier
import pytest

PROJECT_ROOT = Path(__file__).parent.parent


def test_rust_fully_templated(
    tmp_path: Path, rust_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / rust_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=rust_base_answers,
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


def test_rust_constant_file_content(
    tmp_path: Path, rust_base_answers: dict[str, str | bool], helpers
):
    dst_path = tmp_path / rust_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data=rust_base_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    project_name = rust_base_answers["project_name"]
    readme_path = dst_path / "README.md"
    cargo_path = dst_path / "Cargo.toml"
    library_path = dst_path / "src" / "lib.rs"
    binary_path = dst_path / "src" / "main.rs"
    additional_binary_path = dst_path / "src" / "bin"

    helpers.assert_file_content(readme_path, [f"# {project_name}"])
    helpers.assert_file_content(
        cargo_path,
        [
            f"name = \"{project_name.replace(' ', '_').replace('.', '_').replace('-', '_').lower()}\"",  # noqa: E501
            "[lib]",
            "[[bin]]",
        ],
    )

    assert library_path.exists()
    assert binary_path.exists()
    assert additional_binary_path.exists()


@pytest.mark.parametrize(("targets"), ["Library", "Binary"])
def test_rust_targets(
    tmp_path: Path, rust_base_answers: dict[str, str | bool], helpers, targets
):
    dst_path = tmp_path / rust_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**rust_base_answers, "rust_targets": targets},
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()
    cargo_path = dst_path / "Cargo.toml"
    library_path = dst_path / "src" / "lib.rs"
    binary_path = dst_path / "src" / "main.rs"
    additional_binary_path = dst_path / "src" / "bin"

    if targets == "Library":
        assert not binary_path.exists()
        assert not additional_binary_path.exists()
        assert library_path.exists()
        helpers.assert_file_content(
            cargo_path,
            [
                "[lib]",
            ],
            [
                "[[bin]]",
            ],
        )

    if targets == "Binary":
        assert binary_path.exists()
        assert additional_binary_path.exists()
        assert not library_path.exists()
        helpers.assert_file_content(
            cargo_path,
            [
                "[[bin]]",
            ],
            [
                "[lib]",
            ],
        )


@pytest.mark.parametrize(("include_example"), [True, False])
def test_rust_examples(
    tmp_path: Path, rust_base_answers: dict[str, str | bool], include_example
):
    dst_path = tmp_path / rust_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**rust_base_answers, "rust_include_examples": include_example},
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()

    example_path = dst_path / "examples"

    if not include_example:
        assert not example_path.exists()

    else:
        assert example_path.exists()


@pytest.mark.parametrize(("include_benchmark"), [True, False])
def test_rust_benchmarks(
    tmp_path: Path, rust_base_answers: dict[str, str | bool], helpers, include_benchmark
):
    dst_path = tmp_path / rust_base_answers["project_name"]
    worker = copier.run_copy(
        src_path=str(PROJECT_ROOT),
        dst_path=dst_path,
        data={**rust_base_answers, "rust_include_benchmark": include_benchmark},
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert dst_path.exists()

    benches_path = dst_path / "benches"
    cargo_path = dst_path / "Cargo.toml"

    if not include_benchmark:
        assert not benches_path.exists()
        helpers.assert_file_content(
            cargo_path,
            ["bench = false"],
            ["bench = true"],
        )

    else:
        assert benches_path.exists()
        helpers.assert_file_content(
            cargo_path,
            ["bench = true"],
            ["bench = false"],
        )
