"""Tests for extracting the METADATA file from a built wheel."""
import zipfile

import pytest

from tools_src.package_creator import get_wheel_metadata

METADATA = b"Metadata-Version: 2.1\nName: arm-none-eabi-gcc-toolchain\nVersion: 14.2.1\n"


def make_wheel(path, entries):
    with zipfile.ZipFile(path, "w") as wheel:
        for name, data in entries.items():
            wheel.writestr(name, data)
    return path


def test_returns_the_wheels_metadata_bytes(tmp_path):
    wheel = make_wheel(
        tmp_path / "pkg-14.2.1-py3-none-any.whl",
        {
            "arm_none_eabi_gcc_toolchain/__init__.py": b"",
            "pkg-14.2.1.dist-info/METADATA": METADATA,
            "pkg-14.2.1.dist-info/RECORD": b"",
        },
    )

    assert get_wheel_metadata(wheel) == METADATA


def test_missing_metadata_raises(tmp_path):
    wheel = make_wheel(tmp_path / "broken.whl", {"pkg/__init__.py": b""})

    with pytest.raises(FileNotFoundError):
        get_wheel_metadata(wheel)
