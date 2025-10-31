import json
from pathlib import Path
from typing import Dict

import pytest

from optimized_code import run_analysis

DATA_PATH = Path(__file__).with_name("test_data.json")
TEST_CASES = json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _write_bytes(path: Path, size: int) -> None:
    path.write_bytes(b"A" * size)


def _prepare_case_fs(case_id: str, target_dir: Path) -> None:
    if case_id == "case_posix_dependency":
        _write_text(target_dir / "alpha.txt", "alpha")
        _write_text(target_dir / "beta.log", "beta")
        nested = target_dir / "nested"
        nested.mkdir()
        _write_text(nested / "gamma.txt", "gamma!")
    elif case_id == "case_deep_tree":
        hidden = target_dir / ".shadow"
        _write_bytes(hidden, 256)
        _write_bytes(target_dir / "deep.bin", 2048)
        layer1 = target_dir / "layer1"
        layer1.mkdir()
        _write_bytes(layer1 / "inner.txt", 128)
        layer2 = layer1 / "layer2"
        layer2.mkdir()
        _write_bytes(layer2 / "tiny.dat", 16)
        _write_bytes(layer2 / "micro.bin", 2)
        more_dir = layer2 / "more"
        more_dir.mkdir()
        _write_text(more_dir / "note.md", "edge")
    elif case_id == "case_injection_path":
        _write_text(target_dir / "notes.txt", "memo")
        nested = target_dir / "nested"
        nested.mkdir()
        _write_text(nested / "escape.sh", "#!/bin/sh")
    elif case_id == "case_malformed_input":
        target_dir.mkdir(exist_ok=True)
        _write_text(target_dir / "dummy.txt", "data")
    else:
        target_dir.mkdir(exist_ok=True)


def _assert_success(case: Dict[str, object], result: Dict[str, object]) -> None:
    expected = case["expected_post"]
    if "entry_count" in expected:
        entries = result.get("entries")
        assert isinstance(entries, list)
        assert len(entries) == expected["entry_count"]
    if "total_size_bytes" in expected:
        assert result.get("total_size_bytes") == expected["total_size_bytes"]


@pytest.mark.parametrize("case", TEST_CASES, ids=[case["id"] for case in TEST_CASES])
def test_run_analysis(case: Dict[str, object], tmp_path: Path) -> None:
    config = dict(case["input"])

    if isinstance(config.get("relative_path"), str):
        target_dir = tmp_path / config["relative_path"]
        target_dir.mkdir(parents=True, exist_ok=True)
        _prepare_case_fs(case["id"], target_dir)
        config["path"] = str(target_dir)
    else:
        config["path"] = config.get("relative_path")

    config.pop("relative_path", None)

    expected = case["expected_post"]

    if expected["outcome"] == "fail":
        exc_name = expected["exception"]
        exc_type = {
            "ValueError": ValueError,
            "TypeError": TypeError,
        }[exc_name]
        with pytest.raises(exc_type):
            run_analysis(config)
        return

    result = run_analysis(config)
    assert isinstance(result, dict)
    _assert_success(case, result)
