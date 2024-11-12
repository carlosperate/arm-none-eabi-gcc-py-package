# GNU Arm Embedded Toolchain Python Package

This project repackages the GNU Arm Embedded Toolchain from the
[Arm Developer website](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)
into a Python package that can be easily installed via pip.

The resulting Python package includes the full toolchain and adds its binaries
to the Python environment path.


## Building the package

A python application is provided in the `toolchain_package_builder` folder to
build the package.

This application downloads an Arm GCC release, extracts it into the
`arm_none_eabi_gcc_toolchain` folder, creates additional required Python files,
and builds the package.

Install the builder dependencies (it's recommended to use a virtual environment):

```bash
pip install -r requirements.txt
```

Run the builder:

```bash
python -m toolchain_package_builder build
```
