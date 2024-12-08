# GNU Arm Embedded Toolchain Python Package

This project repackages the GNU Arm Embedded Toolchain from the
[Arm Developer website](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
into a Python package that can be easily installed via pip.

The resulting Python package includes the full toolchain and adds its binaries
to the Python environment path.

This is still a work-in-progress and doesn't work yet.

## TODO

- [x] Update wheels to have platform labels
- [x] Set up versioning
- [ ] Create GH Action workflow to build and publish the wheels in GH Releases
- [ ] Create a static simple repository ([PEP 503](https://peps.python.org/pep-0503/)) to host the wheels via GitHub (releases+pages)
- [ ] Use or fork [wheel-stub](https://github.com/wheel-next/wheel-stub/) to be able to publish source packages to PyPI
- [ ] Keep an eye on [PEP 759 – External Wheel Hosting](https://peps.python.org/pep-0759/)

## Versioning

The package version follows the format, which combines the GCC version and the
`package_builder` version:

```
MAJOR.MINOR.PATCH
```
Where:
- MAJOR version is the GCC major version
- MINOR version is the GCC minor version
- PATCH version is version of `package_builder` used to create the package

So for example:

```
13 . 3 . 1
└──┬──┘ └┬┘
   │     └──── package_builder version
   └────────── GCC major.minor version
```

This allows version locking to a specific GCC version and the latest
`package_builder` version, e.g. `~=13.3`/`==13.3.*`.

## Building the package

A python application is provided in the `package_builder` folder to
build the package.

This application downloads an Arm GCC release, extracts it into the
`arm_none_eabi_gcc_toolchain` folder, creates additional required Python files,
and builds the `arm_none_eabi_gcc_toolchain` package.

Install the builder dependencies (it's recommended to use a virtual environment):

```bash
pip install -r requirements.txt
```

Run the builder:

```bash
python -m package_builder build
```
