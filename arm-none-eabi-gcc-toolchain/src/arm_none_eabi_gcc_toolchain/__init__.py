# -*- coding:utf-8 -*-
"""
Paths to the bundled Arm GNU Toolchain for build scripts that want the real
binaries rather than the ``arm-none-eabi-*`` launchers.

Tries to keep import-time work as low as possible, as all executable shims
will import this module.
"""
import os
import sys

__all__ = ["toolchain_dir", "bin_dir", "executable"]

# Where the toolchain folder is looked for; tests point this at a fake install
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
_PREFIX = "arm-none-eabi-"
_EXE = ".exe" if sys.platform == "win32" else ""


def toolchain_dir():
    """Absolute path to the root folder of the bundled toolchain."""
    # The folder name varies per GCC release, so locate it by content
    for entry in os.listdir(PACKAGE_DIR):
        candidate = os.path.join(PACKAGE_DIR, entry)
        if os.path.isfile(os.path.join(candidate, "bin", f"{_PREFIX}gcc{_EXE}")):
            return candidate
    raise FileNotFoundError("Arm GNU Toolchain not found inside " + PACKAGE_DIR)


def bin_dir():
    """Absolute path to the toolchain ``bin`` folder."""
    return os.path.join(toolchain_dir(), "bin")


def executable(name):
    """Absolute path to a toolchain binary, e.g. ``executable("gcc")``."""
    if not name.startswith(_PREFIX):
        name = _PREFIX + name
    if _EXE and not name.endswith(_EXE):
        name += _EXE
    path = os.path.join(bin_dir(), name)
    if not os.path.isfile(path):
        raise FileNotFoundError("Toolchain executable not found: " + path)
    return path
