"""
Tests for the distributed package's __init__.py against a fake toolchain
folder laid out the way a wheel installs it. No real toolchain is needed.
"""
import sys

import pytest

# The source tree has no toolchain folder, so this import must not scan for one
import arm_none_eabi_gcc_toolchain as pkg

EXE = ".exe" if sys.platform == "win32" else ""
GCC = "arm-none-eabi-gcc" + EXE
GXX = "arm-none-eabi-g++" + EXE

# Folder names differ between GCC releases; the package must cope with any
TOOLCHAIN_FOLDER_NAMES = [
    "arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi",
    "gcc-arm-none-eabi-9-2019-q4-major",
]


@pytest.fixture
def pkg_dir(tmp_path, monkeypatch):
    """The installed package directory as pip lays it out, minus the toolchain."""
    path = tmp_path / "site-packages" / "arm_none_eabi_gcc_toolchain"
    path.mkdir(parents=True)
    (path / "__pycache__").mkdir()
    monkeypatch.setattr(pkg, "PACKAGE_DIR", str(path))
    return path


@pytest.fixture(params=TOOLCHAIN_FOLDER_NAMES)
def toolchain(request, pkg_dir):
    """A fake toolchain folder inside the package with a couple of binaries."""
    root = pkg_dir / request.param
    (root / "bin").mkdir(parents=True)
    (root / "bin" / GCC).touch()
    (root / "bin" / GXX).touch()
    return root


def test_paths_point_inside_the_installed_toolchain(toolchain):
    assert pkg.toolchain_dir() == str(toolchain)
    assert pkg.bin_dir() == str(toolchain / "bin")


def test_executable_accepts_short_and_full_names(toolchain):
    gcc = str(toolchain / "bin" / GCC)
    assert pkg.executable("gcc") == gcc
    assert pkg.executable("arm-none-eabi-gcc") == gcc
    assert pkg.executable(GCC) == gcc
    assert pkg.executable("g++") == str(toolchain / "bin" / GXX)


def test_missing_executable_raises(toolchain):
    with pytest.raises(FileNotFoundError):
        pkg.executable("ld")


def test_missing_toolchain_raises(pkg_dir):
    with pytest.raises(FileNotFoundError):
        pkg.bin_dir()
