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

## License

All the source code to create this Python package is licensed under the
MIT license.

The generated wheels contain the GNU Arm Embedded Toolchain, licensed under
the GPL v3 license.
