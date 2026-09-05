"""
Tests for the generated ``run_*.py`` launchers. The template is rendered the
way package_creator does it, pointed at a stand-in tool, and run as a process.
"""
import sys
import subprocess
from pathlib import Path

import pytest

TEMPLATE = (
    Path(__file__).resolve().parents[1]
    / "arm-none-eabi-gcc-toolchain"
    / "src"
    / "arm_none_eabi_gcc_toolchain"
    / "executable_launcher.py.txt"
)
WINDOWS = sys.platform == "win32"
TOOL = "arm-none-eabi-gcc.bat" if WINDOWS else "arm-none-eabi-gcc"
# Stand-in tool: prints its PID (POSIX only) and its arguments, then exits with 3
FAKE_TOOL = "@echo %*\r\n@exit /b 3\r\n" if WINDOWS else '#!/bin/sh\necho $$\necho "$@"\nexit 3\n'


@pytest.fixture
def launcher(tmp_path):
    """A rendered run_gcc.py next to a fake toolchain folder, as in an install."""
    pkg = tmp_path / "arm_none_eabi_gcc_toolchain"
    tool = pkg / "toolchain-folder" / "bin" / TOOL
    tool.parent.mkdir(parents=True)
    tool.write_text(FAKE_TOOL)
    tool.chmod(0o755)
    script = pkg / "run_gcc.py"
    script.write_text(
        TEMPLATE.read_text().format(
            bin=TOOL, func_name="run_gcc", gcc_folder="toolchain-folder"
        )
    )
    return script


def run(launcher, *args):
    return subprocess.run(
        [sys.executable, str(launcher), *args], stdout=subprocess.PIPE, text=True
    )


def test_arguments_and_exit_code_are_forwarded(launcher):
    result = run(launcher, "-O2", "main.c")

    assert result.returncode == 3
    assert "-O2 main.c" in result.stdout


@pytest.mark.skipif(WINDOWS, reason="Windows cannot exec; the tool runs as a child")
def test_tool_replaces_the_launcher_process(launcher):
    process = subprocess.Popen(
        [sys.executable, str(launcher)], stdout=subprocess.PIPE, text=True
    )
    stdout, _ = process.communicate()

    assert int(stdout.split()[0]) == process.pid
