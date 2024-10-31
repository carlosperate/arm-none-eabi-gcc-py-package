package_pyproject = """
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "arm_none_eabi_gcc_toolchain"
version = "0.1.0"
description = "Arm GNU Toolchain (arm-none-eabi-gcc)"
authors = [
    {{ name = "Carlos Pereira Atencio", email = "carlosperate@embeddedlog.com" }}
]
readme = {{file = "README.md", content-type = "text/markdown"}}
license = {{"file" = "LICENSE"}}

# The individual executables will be added here
[project.scripts]
{pyproject_scripts}

[tool.setuptools]
include-package-data = true

[tool.setuptools.dynamic]
readme = {{file = ["README.md"]}}

[tool.setuptools.packages.find]
where = ["{gcc_folder}"]
"""

executable_launcher = """
import os
import sys
import subprocess


def launch_{bin_short}():
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
    launch_{bin_short}()
"""
