# GNU Arm Embedded Toolchain Python Package

This project repackages the GNU Arm Embedded Toolchain from the
[Arm Developer website](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
into a Python package that can be easily installed via pip.

The resulting Python package includes the full toolchain and adds its binaries
to the Python environment path.

## Table of Contents

- [Current project state](#current-project-state)
- [Installation](#installation)
- [Versions and Platforms](#versions-and-platforms)
- [Why?](#why)
- [Project/repository structure](#projectrepository-structure)
- [Building the package](#building-the-package)
- [Building the Simple Repository](#building-the-simple-repository)
- [License](#license)

## Current project state

> [!CAUTION]
> This is still a work-in-progress, the package is not yet available on PyPI,
> and any pre-release versions installed right now might be broken.

There is currently a simple repository with the package available at
https://carlosperate.github.io/arm-none-eabi-gcc-py-package.

So, at the moment, to install the package we need to use the
`--extra-index-url` flag.

Because the wheels size is larger than the default PyPI max size, the next
step would be to find a way to be able to publish a package to PyPI that's
able to pull the wheels from an external source.

TODO list:

- [ ] Use or fork [wheel-stub](https://github.com/wheel-next/wheel-stub/) to
  publish source packages to PyPI that pull these wheels externally hosted
- [ ] Keep an eye on [PEP 759 – External Wheel Hosting](https://peps.python.org/pep-0759/)

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

## Versions and Platforms

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
GCC version and the `package_builder` versions, where:
- MAJOR version is the GCC major version
- MINOR version is the GCC minor version
- PATCH version is a single number indicating the version of `package_builder`
  used to create the package

So for example:

```
13 . 3 . 1
└──┬──┘ └┬┘
   │     └──── package_builder version
   └────────── GCC major.minor version
```

This allows version locking to a specific GCC version and be able to fetch the
latest `package_builder` (which might include bug fixes in the packaging),
e.g. `~=13.3`/`==13.3.*`.

## Why?

With tools like CMake and Ninja already available via PyPI, this package
completes the ecosystem for embedded development, making it possible to manage
embedded project tooling entirely through Python packaging.

And while Python packaging is far from perfect, it provides some advantages:

- If your project already uses Python you can manage the toolchain alongside
  other project dependencies
- You can lock a specific toolchain version to the project requirements
- Easily install or update the toolchain via pip/pipx/uv, without relying on
  the tool version being available in the OS package manager
    - It can sometimes be challenging to get an older versions of a tool in
      a recent OS release, or a newer versions in older OS releases
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
  package source code, the rest of the package data is generated by
  `package_builder`.
- `package_builder`: Contains the Python scripts used to generate the 
  complete `arm-none-eabi-gcc-toolchain` packages (which are later
  uploaded to GH releases via CI).
- `simple_repository_generator`: Contains the Python scripts used to generate
  the static HTML pages for a [PEP 503](https://peps.python.org/pep-0503/)
  Python simple package repository, which links to the wheels
  stored in the GH Releases. This repository is published to GH Pages via CI.
- `arm-none-eabi-gcc-toolchain-pypi`: Contains the files to create a secondary
   package, which uses [wheel-stub](https://github.com/wheel-next/wheel-stub)
   to create a source distribution package to be published to PyPI.
   When this package is installed wheel-stub downloads and installs the
   platform-specific wheels from this project Simple Repository.

## Building the package

The `package_builder` folder contains the Python scripts needed to build
the package.

This script downloads an Arm GCC release, extracts it within the
`arm-none-eabi-gcc-toolchain` package folder, creates the additional Python
files required for the package, and builds it.

Install the builder dependencies (it's recommended to use a virtual environment):

```bash
pip install -r requirements.txt
```

Run the builder:

```bash
python -m package_builder build --release <name_of_release> --os <operating system> --arch <cpu architecture>
```

Options are:
- `--release`: The GCC release name as shown in the [versions section](#versions)
- `--os`: `linux`, `mac`, or `win`
- `--arch`: `x86_64` or `aarch64`/`arm64`

## Building the PyPI Source Distribution

The `arm-none-eabi-gcc-toolchain-pypi` folder contains the `pyproject.toml`
needed to create a secondary package, which uses
[wheel-stub](https://github.com/wheel-next/wheel-stub) to create a source
distribution package to be published to PyPI.

To build the source distribution package, build a `arm-none-eabi-gcc-toolchain`
wheel and run the following command:

```bash
cd arm-none-eabi-gcc-toolchain-pypi
python -m build --sdist --config-setting source_wheel=../dist/wheel_file.whl
```

## Building the Simple Repository

The `simple_repository_regenerator` folder contains the Python scripts
used to generate a [PEP 503](https://peps.python.org/pep-0503/) and
[PEP 629](https://peps.python.org/pep-0629/) compliant (it does **not**
implement [PEP 691](https://peps.python.org/pep-0691/) JSON format)
static HTML python package repository site that points to the wheels
stored in the GitHub Releases from this repository.

To generate the HTML output, run the following command:

```bash
python -m simple_repository_generator "carlosperate/arm-none-eabi-gcc-py-package"
```

## License

All the source code in this repository is licensed under the MIT license.

The generated wheels contain the GNU Arm Embedded Toolchain,
which is licensed under the GPL v3 license.
