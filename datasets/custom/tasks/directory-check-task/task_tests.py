import os
import shutil
import subprocess
import tempfile

SCRIPT_PATH = "scripts/run_directory_check.sh"

def run_script(base_dir):
    return subprocess.run(
        ["bash", SCRIPT_PATH, "python"],
        cwd=base_dir,
        capture_output=True,
        text=True
    )


def create_valid_structure(base_dir):
    path = os.path.join(
        base_dir,
        "tmp.benchmarks/polyglot-benchmark/python/exercises/practice/sample1"
    )

    os.makedirs(os.path.join(path, ".docs"), exist_ok=True)
    os.makedirs(os.path.join(path, ".meta"), exist_ok=True)
    os.makedirs(os.path.join(path, "test-file-logs"), exist_ok=True)

    open(os.path.join(path, ".docs/instructions.md"), "w").write("ok")
    open(os.path.join(path, ".docs/introduction.md"), "w").write("ok")
    open(os.path.join(path, ".meta/config.json"), "w").write("{}")

    open(os.path.join(path, "sample1.py"), "w").write("print(1)")
    open(os.path.join(path, "sample1_test.py"), "w").write("assert True")

    open(os.path.join(path, "test-file-logs/negative_test1.py"), "w").write("bad")
    open(os.path.join(path, "test-file-logs/negative_test1_output.txt"), "w").write("error")


def test_valid_structure_passes():
    with tempfile.TemporaryDirectory() as tmp:
        create_valid_structure(tmp)

        result = run_script(tmp)

        assert result.returncode == 0, result.stdout


def test_missing_required_file_fails():
    with tempfile.TemporaryDirectory() as tmp:
        create_valid_structure(tmp)

        os.remove(os.path.join(
            tmp,
            "tmp.benchmarks/polyglot-benchmark/python/exercises/practice/sample1/.meta/config.json"
        ))

        result = run_script(tmp)

        assert result.returncode != 0


def test_empty_file_fails():
    with tempfile.TemporaryDirectory() as tmp:
        create_valid_structure(tmp)

        open(os.path.join(
            tmp,
            "tmp.benchmarks/polyglot-benchmark/python/exercises/practice/sample1/.docs/instructions.md"
        ), "w").close()

        result = run_script(tmp)

        assert result.returncode != 0


def test_missing_directory_fails():
    with tempfile.TemporaryDirectory() as tmp:
        create_valid_structure(tmp)

        shutil.rmtree(os.path.join(
            tmp,
            "tmp.benchmarks/polyglot-benchmark/python/exercises/practice/sample1/test-file-logs"
        ))

        result = run_script(tmp)

        assert result.returncode != 0