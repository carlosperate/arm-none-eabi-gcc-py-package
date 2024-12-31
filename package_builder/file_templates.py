#!/usr/bin/env python3
# -*- coding:utf-8 -*-

executable_launcher = """
import os
import sys
import subprocess


def {func_name}():
    argv = [
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "{gcc_folder}",
            "bin",
            "{bin}"
        ),
        *sys.argv[1:]
    ]
    exit_code = subprocess.call(argv)
    sys.exit(exit_code)


if __name__ == "__main__":
    {func_name}()
"""

manifest_in = """
recursive-include src/arm_none_eabi_gcc_toolchain/{gcc_folder} *
"""

pyproject_toml = """
[build-system]
requires = ["setuptools >= 61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "arm-none-eabi-gcc-toolchain"
version = "{version}"
description = "The Arm GNU Toolchain (arm-none-eabi-gcc) to cross-compile for ARM Cortex-M microcontrollers."
authors = [
    {{ name = "Carlos Pereira Atencio", email = "carlosperate@embeddedlog.com" }}
]
readme = "README.md"
license = {{ text = "MIT License" }}
keywords = ["gcc", "arm-none-eabi-gcc", "build", "c", "c++", "cross-compilation"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Topic :: Software Development :: Build Tools",
    "Topic :: Software Development :: Compilers",
    "Programming Language :: C",
    "Programming Language :: C++",
    "Programming Language :: Python :: 3",
]

[project.urls]
Homepage = "https://github.com/carlosperate/arm-none-eabi-gcc-py-package"
Repository = "https://github.com/carlosperate/arm-none-eabi-gcc-py-package.git"
Issues = "https://github.com/carlosperate/arm-none-eabi-gcc-py-package/issues"

# A script entry for each individual GCC executable will be added to this table
[project.scripts]
{bin_scripts}
"""
