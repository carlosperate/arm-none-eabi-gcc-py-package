# GNU Arm Embedded Toolchain Python Package

This project repackages the GNU Arm Embedded Toolchain from the
[Arm Developer website](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
into a Python package that can be easily installed via pip.

The resulting Python package includes the full toolchain and adds its binaries
to the Python environment path.

<p align="center"><img src="https://github.com/user-attachments/assets/47db670d-b313-4f83-9616-418b32cadef6" alt="CLI animation installing and using compiler" width="85%"></p>

## Table of Contents

- [Current project state](#current-project-state)
- [Installation](#installation)
- [Versions and platforms](#versions-and-platforms)
- [Why?](#but-why)
- [Project/repository structure](#projectrepository-structure)
- [Building the project](#building-the-project)
- [License](#license)

## Current project state

> [!CAUTION]
> This is still a work-in-progress, the package is not yet available on PyPI,
> and any pre-release versions installed right now might be broken.

There is currently a simple Python package repository with the available
package at https://carlosperate.github.io/arm-none-eabi-gcc-py-package.

So, right now, to install the package we need to use the
`--extra-index-url` pip install flag.

Because the size of the generated wheels is larger than the default PyPI
maximum, the [wheel-stub](https://github.com/wheel-next/wheel-stub/) project
is used to create a source distribution that can be pushed to PyPI.
During package installation, wheel-stub acts as a package build back-end
that downloads the corresponding wheel from the external package repository.

This is currently tested and set up with the Test PyPI repository,
but it has not been released yet in the real PyPI.

Outstanding tasks are captured in the
[GitHub issues tracker](https://github.com/carlosperate/arm-none-eabi-gcc-py-package/issues).

## Installation

In its currents state we need to use an extra index URL to install the package:
```
pip install arm-none-eabi-gcc-toolchain --extra-index-url https://carlosperate.github.io/arm-none-eabi-gcc-py-package
```

And all the GNU Arm Embedded Toolchain binaries will be available in the path:
```
$ which arm-none-eabi-gcc
(...)/.venv/bin/arm-none-eabi-gcc

$ arm-none-eabi-gcc --version
arm-none-eabi-gcc (Arm GNU Toolchain 13.3.Rel1 (Build arm-13.24)) 13.3.1 20240614
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ arm-none-eabi-<tab>
…one-eabi-addr2line         (command)  …one-eabi-gdb-add-index     (command)
…one-eabi-ar                (command)  …one-eabi-gdb-add-index-py  (command)
…one-eabi-as                (command)  …one-eabi-gdb-py            (command)
…one-eabi-c++               (command)  …one-eabi-gfortran          (command)
…one-eabi-c++filt           (command)  …one-eabi-gprof             (command)
…one-eabi-cpp               (command)  …one-eabi-ld                (command)
…one-eabi-elfedit           (command)  …one-eabi-ld.bfd            (command)
…one-eabi-g++               (command)  …one-eabi-lto-dump          (command)
…one-eabi-gcc               (command)  …one-eabi-nm                (command)
…one-eabi-gcc-13.3.1        (command)  …one-eabi-objcopy           (command)
…one-eabi-gcc-ar            (command)  …one-eabi-objdump           (command)
…one-eabi-gcc-nm            (command)  …one-eabi-ranlib            (command)
…one-eabi-gcc-ranlib        (command)  …one-eabi-readelf           (command)
…one-eabi-gcov              (command)  …one-eabi-size              (command)
…one-eabi-gcov-dump         (command)  …one-eabi-strings           (command)
…one-eabi-gcov-tool         (command)  …one-eabi-strip             (command)
…one-eabi-gdb               (command)
```

## Versions and platforms

| GCC Version  | Python Package Version | Win x86_64 | Linux x86_64 | Linux aarch64 |  macOS x86_64 | macOS arm64 |
|--------------|------------------------|------------|--------------|---------------|---------------|-------------|
| 13.3.Rel1    | 13.3.*                 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 13.2.Rel1    | 13.2.*                 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 12.3.Rel1    | 12.3.*                 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 12.2.Rel1    | 12.2.*                 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 11.3.Rel1    | 11.3.*                 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 11.2-2022.02 | 11.2.*                 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 10.3-2021.10 | 10.3.*                 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 10-2020-q4   | 10.2.*                 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 9-2020-q2    | 9.3.*                  | ✅ | ✅ | ✅ | ✅ | ❌ |
| 9-2019-q4    | 9.2.*                  | ✅ | ✅ | ✅ | ✅ | ❌ |

### Versioning scheme

The package version follows `MAJOR.MINOR.PATCH` format, but it combines the
GCC version and the `package_creator` versions together, where:
- MAJOR version is the GCC major version
- MINOR version is the GCC minor version
- PATCH version is a single number indicating the version of `package_creator`
  used to create the package

```
13 . 3 . 1
└──┬──┘ └┬┘
   │     └──── package_creator version
   └────────── GCC major.minor version
```

This allows version locking to a specific GCC version and be able to fetch the
released created with the latest `package_creator`,
which might include bug fixes in the packaging, e.g. `~=13.3`/`==13.3.*`.

## But why?

<img src="https://github.com/user-attachments/assets/86be2c45-f2e5-4f01-9fc6-c3a6f9c040e0" alt="But Why meme" align="right" width="15%">

With tools like CMake and Ninja already available via PyPI, this package
adds to the ecosystem a compiler for embedded development, making it possible
to manage embedded project tooling entirely through Python packaging.

And while Python packaging is far from perfect, it provides some advantages:

- If your project already uses Python you can manage the toolchain alongside
  other project dependencies
- You can lock a specific toolchain version to the project requirements
- Easily install or update the toolchain via pip/pipx/uv, without relying on
  the tool version being available in the OS package manager
    - It can sometimes be challenging to get an older versions of a tool in
      a recent OS release, or a newer version in old OS release
- Leverage Python virtual environments to manage different toolchain versions
  per project on the same system
- Simplify cross-platform toolchain installation by using the same package
  manager across all platforms
    - This is also useful for CI pipelines, including matrix jobs testing
      multiple versions of different tools with the same project

## Project/repository structure

There are multiple folders in this repository to serve different aspects of
this package creation and distribution:

- `arm-none-eabi-gcc-toolchain`: Contains the skeleton code for the Python
  package metadata and source code, the rest of the package data is generated
  by the tooling in this project.
- `arm-none-eabi-gcc-toolchain-pypi`: Contains the files to create a secondary
   package, which uses [wheel-stub](https://github.com/wheel-next/wheel-stub)
   to create a source distribution to be published to PyPI.
   When this package is installed from PyPI via pip, wheel-stub downloads and
   installs the platform-specific wheels from this project package repository.
- `tools_src`: Contains the Python scripts used mainly for two purposes.
    - `package_creator`: Generates the complete `arm-none-eabi-gcc-toolchain`
      package files, builds the wheels, and generates the PyPI source
      distribution (all are uploaded to GH releases via CI).
    - `simple_repository_generator`: Generates the static HTML pages for a
      [PEP 503](https://peps.python.org/pep-0503/) Python simple package
      repository, which links to the wheels stored in this repo GH Releases.
      This repository is published to GH Pages via CI.

## Building the project

### Installing dependencies

Recommended to use a virtual environment:

```bash
pip install -r requirements.txt
```

### Building the wheels

The scripts in the `tools_src` folder download the Arm GCC release,
extracts it within the `arm-none-eabi-gcc-toolchain` package folder, creates
the additional Python files required for the package, and builds it in the
a `dist` folder in the project root directory.

Run the builder:

```bash
python tools.py package-creator <name_of_release> --os <operating system> --arch <cpu architecture>
```

The first argument (shown as `<name_of_release>`) is the GCC release name as
shown in the [versions section](#versions-and-platforms).

All flags are optional, `all` builds wheels for all platforms.
The `os` and `arch` specify a platform version of the package,
both or neither must be used.
- `--os`: `linux`, `mac`, or `win`
- `--arch`: `x86_64` or `aarch64`/`arm64`

### Building the PyPI source distribution

The `arm-none-eabi-gcc-toolchain-pypi` folder contains the `pyproject.toml`
needed to create a secondary package, which uses
[wheel-stub](https://github.com/wheel-next/wheel-stub) to create a source
distribution package to be published to PyPI.

The `package_creator` command will automatically create the source distribution
(`arm_none_eabi_gcc_toolchain-*.tar.gz`) in the `dist` folder next to the wheels.

### Building the Simple Repository

The `repo-generate` command generates a [PEP 503](https://peps.python.org/pep-0503/),
[PEP 629](https://peps.python.org/pep-0629/), [PEP 658](https://peps.python.org/pep-0658/),
and [PEP 714](https://peps.python.org/pep-0714/) compliant static HTML Python
package repository, which points to the wheels
stored in the [GitHub Releases](https://github.com/carlosperate/arm-none-eabi-gcc-py-package/releases/).
This package repository does **not** implement
[PEP 691](https://peps.python.org/pep-0691/) (JSON format).

To generate the HTML output, run the following command:

```bash
python tools.py repo-generate
```

## License

All the source code in this repository is licensed under the [MIT license](LICENSE).

The generated wheels contain the GNU Arm Embedded Toolchain,
which is licensed under the GPL v3 license.
