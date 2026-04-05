from pathlib import Path
import shutil
import subprocess
import tempfile

TASK_DIR = Path(__file__).resolve().parent
REPO_DIR = TASK_DIR / "repo"
SCRIPT_PATH = REPO_DIR / "scripts" / "run_directory_check.sh"
FIXTURE_ROOT = REPO_DIR / "tmp.benchmarks" / "polyglot-benchmark"


def make_temp_fixture():
    temp_dir = tempfile.TemporaryDirectory()
    temp_root = Path(temp_dir.name)

    target_root = temp_root / "tmp.benchmarks" / "polyglot-benchmark"
    shutil.copytree(FIXTURE_ROOT, target_root)

    return temp_dir, temp_root

def run_script(base_dir: Path, language: str):
    return subprocess.run(
        ["bash", str(SCRIPT_PATH), language],
        cwd=base_dir,
        capture_output=True,
        text=True,
    )


# ======== CPP ========

def test_valid_structure_passes_cpp():
    temp_dir, temp_root = make_temp_fixture()
    try:
        result = run_script(temp_root, "cpp")
        assert result.returncode == 0, (
            f"\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    finally:
        temp_dir.cleanup()

def test_missing_required_file_fails_cpp():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_file = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "cpp"
            / "exercises"
            / "practice"
            / "cpp001"
            / ".meta"
            / "config.json"
        )
        bad_file.unlink()

        result = run_script(temp_root, "cpp")
        assert result.returncode != 0, "Expected script to fail when config.json is missing"
    finally:
        temp_dir.cleanup()

def test_empty_file_fails_cpp():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_file = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "cpp"
            / "exercises"
            / "practice"
            / "cpp001"
            / ".docs"
            / "instructions.md"
        )
        bad_file.write_text("")

        result = run_script(temp_root, "cpp")
        assert result.returncode != 0, "Expected script to fail when instructions.md is empty"
    finally:
        temp_dir.cleanup()

def test_missing_directory_fails_cpp():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_dir = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "cpp"
            / "exercises"
            / "practice"
            / "cpp001"
            / "test-file-logs"
        )
        shutil.rmtree(bad_dir)

        result = run_script(temp_root, "cpp")
        assert result.returncode != 0, "Expected script to fail when test-file-logs is missing"
    finally:
        temp_dir.cleanup()


# ======== Go ========

def test_valid_structure_passes_go():
    temp_dir, temp_root = make_temp_fixture()
    try:
        result = run_script(temp_root, "go")
        assert result.returncode == 0, (
            f"\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    finally:
        temp_dir.cleanup()

def test_missing_required_file_fails_go():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_file = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "go"
            / "exercises"
            / "practice"
            / "go001"
            / ".meta"
            / "example.go"
        )
        bad_file.unlink()

        result = run_script(temp_root, "go")
        assert result.returncode != 0, "Expected script to fail when example.go is missing"
    finally:
        temp_dir.cleanup()

def test_empty_file_fails_go():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_file = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "go"
            / "exercises"
            / "practice"
            / "go001"
            / ".docs"
            / "introduction.md"
        )
        bad_file.write_text("")

        result = run_script(temp_root, "go")
        assert result.returncode != 0, "Expected script to fail when introduction.md is empty"
    finally:
        temp_dir.cleanup()

def test_missing_directory_fails_go():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_dir = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "go"
            / "exercises"
            / "practice"
            / "go001"
            / ".test-file-logs"
        )
        shutil.rmtree(bad_dir)

        result = run_script(temp_root, "go")
        assert result.returncode != 0, "Expected script to fail when .test-file-logs is missing"
    finally:
        temp_dir.cleanup()


# ======== Swift ========

def test_valid_structure_passes_swift():
    temp_dir, temp_root = make_temp_fixture()
    try:
        result = run_script(temp_root, "swift")
        assert result.returncode == 0, (
            f"\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    finally:
        temp_dir.cleanup()

def test_missing_required_file_fails_swift():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_file = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "swift"
            / "exercises"
            / "practice"
            / "swift001"
            / ".meta"
            / "Sources"
            / "swift001"
            / "example.swift"
        )
        bad_file.unlink()

        result = run_script(temp_root, "swift")
        assert result.returncode != 0, "Expected script to fail when example.swift is missing"
    finally:
        temp_dir.cleanup()

def test_empty_file_fails_swift():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_file = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "swift"
            / "exercises"
            / "practice"
            / "swift001"
            / "Tests"
            / "Testswift001"
            / "Testswift001.swift"
        )
        bad_file.write_text("")

        result = run_script(temp_root, "swift")
        assert result.returncode != 0, "Expected script to fail when Testswift001.swift is empty"
    finally:
        temp_dir.cleanup()

def test_missing_directory_fails_swift():
    temp_dir, temp_root = make_temp_fixture()
    try:
        bad_dir = (
            temp_root
            / "tmp.benchmarks"
            / "polyglot-benchmark"
            / "swift"
            / "exercises"
            / "practice"
            / "swift001"
            / "test-file-logs"
        )
        shutil.rmtree(bad_dir)

        result = run_script(temp_root, "swift")
        assert result.returncode != 0, "Expected script to fail when test-file-logs is missing"
    finally:
        temp_dir.cleanup()
