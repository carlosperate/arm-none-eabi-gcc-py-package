# GNU Arm Embedded Toolchain (arm-none-eabi-gcc) Python Package

This Python package wraps the [Arm GNU Toolchain](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
to be easily installable via pip and PyPI.

Documentation can be found in the [repository README](https://github.com/carlosperate/arm-none-eabi-gcc-py-package).

<p align="center"><img src="https://github.com/user-attachments/assets/47db670d-b313-4f83-9616-418b32cadef6" alt="CLI animation installing and using compiler" width="85%"></p>

## Installation

During testing this package is only available via Test PyPI, and the pip
install command needs the "extra index URL" flag:

```
pip install --extra-index-url https://test.pypi.org/simple/ arm-none-eabi-gcc-toolchain
```

Because the Python wheels containing the toolchain are larger than the default
maximum size allowed by PyPI, a source distribution is provided instead.

When pip installs this source distribution, it uses
[wheel-stub](https://github.com/wheel-next/wheel-stub) as its build backend to
download and install the correct wheel from an external Python Package
Repository set up for this purpose:
https://carlosperate.github.io/arm-none-eabi-gcc-py-package/

## Using the toolchain from Python

The `arm-none-eabi-*` commands on the path are small Python launchers.
Build scripts that call the compiler many times, or that need to give CMake
a real compiler path, can ask the package where the binaries are:

```python
import os
import subprocess
import arm_none_eabi_gcc_toolchain as toolchain

# Path to one tool executable
gcc = toolchain.executable("gcc")

# Or put every tool on the PATH of a child process
env = dict(os.environ)
env["PATH"] = toolchain.bin_dir() + os.pathsep + env["PATH"]
subprocess.run(["cmake", "-DCMAKE_C_COMPILER=" + gcc, ".."], env=env)
```

`toolchain_dir()` returns the root folder of the bundled toolchain and
`bin_dir()` its `bin` folder, both as absolute path strings.

## Versions and platforms

| Package Version | GCC Version  | Win x86_64 | Linux x86_64 | Linux aarch64 | macOS x86_64 | macOS arm64 |
|-----------------|--------------|------------|--------------|---------------|--------------|-------------|
| 14.2.*          | 14.2.Rel1    | ✅ | ✅ | ✅ | ✅ | ✅ |
| 13.3.*          | 13.3.Rel1    | ✅ | ✅ | ✅ | ✅ | ✅ |
| 13.2.*          | 13.2.Rel1    | ✅ | ✅ | ✅ | ✅ | ✅ |
| 12.3.*          | 12.3.Rel1    | ✅ | ✅ | ✅ | ✅ | ✅ |
| 12.2.*          | 12.2.Rel1    | ✅ | ✅ | ✅ | ✅ | ✅ |
| 11.3.*          | 11.3.Rel1    | ✅ | ✅ | ✅ | ✅ | ❌ |
| 11.2.*          | 11.2-2022.02 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 10.3.*          | 10.3-2021.10 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 10.2.*          | 10-2020-q4   | ✅ | ✅ | ✅ | ✅ | ❌ |
| 9.3.*           | 9-2020-q2    | ✅ | ✅ | ✅ | ✅ | ❌ |
| 9.2.*           | 9-2019-q4    | ✅ | ✅ | ✅ | ✅ | ❌ |

The package version follows `MAJOR.MINOR.PATCH` format, but it combines the
GCC Toolchain version and the `packaging` versions together, where:
- MAJOR version is the GCC major version
- MINOR version is the GCC minor version
- PATCH version is a single number indicating the version of the packaging
  code used to create the package

```
13 . 3 . 1
└──┬──┘ └┬┘
   │     └──── package_creator version
   └────────── GCC major.minor version
```

This allows version locking to a specific GCC version and be able to fetch the
releases created with the latest packaging, e.g. `~=13.3.1` or `==13.3.*`.

## License

The source code to create this Python package is licensed under MIT license.

The GNU Arm Embedded Toolchain included in the package is licensed under
the GPL v3 license.
