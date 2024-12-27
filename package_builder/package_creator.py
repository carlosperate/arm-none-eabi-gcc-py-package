#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import re
import sys
import hashlib
import tarfile
import zipfile
import platform
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional, List
from collections import namedtuple


import tomli
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)

from package_builder import file_templates
from package_builder import __version__ as package_builder_version
from package_builder.gcc_releases import gcc_releases, gcc_short_versions


PROJECT_NAME = "arm-none-eabi-gcc-toolchain"
PACKAGE_NAME = "arm_none_eabi_gcc_toolchain"
PROJECT_PATH = Path(__file__).resolve().parents[1] / PROJECT_NAME
PACKAGE_PATH = PROJECT_PATH / "src" / PACKAGE_NAME

# NameTuple with the GCC info
GccInfo = namedtuple("GccInfo", ["files", "release_name", "os_arch"])


def get_gcc_releases(
    release_name: Optional[str], os_type: Optional[str], cpu_arch: Optional[str]
) -> List[GccInfo]:
    # Set default values
    if release_name is None:
        # Python dictionaries are now ordered, so the latest release is the first one
        release_name = list(gcc_releases.keys())[0]
    if release_name not in gcc_releases:
        raise ValueError(f"Unrecognised GCC release name: {release_name}")
    if os_type is None:
        os_type = platform.system()
    os_type = os_type.lower()
    if cpu_arch is None:
        cpu_arch = platform.machine()
    cpu_arch = cpu_arch.lower()

    # We have a special case for os_type and cpu_arch being set to "all"
    # but error if only one of them is set to "all"
    if (os_type == "all" and cpu_arch != "all") or (
        os_type != "all" and cpu_arch == "all"
    ):
        raise ValueError(
            "Both OS type and CPU architecture must be 'all', not just one"
        )
    if os_type == "all" and cpu_arch == "all":
        gcc_release_all = []
        for release_type in gcc_releases[release_name].keys():
            gcc_release_all.append(
                GccInfo(
                    files=gcc_releases[release_name][release_type],
                    release_name=release_name,
                    os_arch=release_type,
                )
            )
        return gcc_release_all

    # Determine CPU architecture
    if cpu_arch in ["x86_64", "amd64", "i386", "i686"]:
        cpu_arch = "x86_64"
    elif cpu_arch in ["arm64", "aarch64", "armv8a", "armv8b", "armv8l"]:
        cpu_arch = "arm"
    else:
        raise ValueError(f"Unrecognised CPU architecture: {cpu_arch}")

    if os_type in ["darwin", "macos", "macosx", "osx", "mac"]:
        if cpu_arch == "x86_64":
            release_type = "mac_x86_64"
        elif cpu_arch == "arm":
            release_type = "mac_arm64"
            # Not all releases have a macOS ARM version
            if release_type not in gcc_releases[release_name]:
                raise ValueError(
                    f"Release {release_name} does not have a macOS arm64 version"
                )
    elif os_type in ["windows", "win", "win32"]:
        if cpu_arch == "x86_64":
            release_type = "win32"
        elif cpu_arch == "arm":
            raise ValueError("Windows ARM architecture not supported")
    elif os_type in ["linux", "linux2"]:
        if cpu_arch == "x86_64":
            release_type = "linux_x86_64"
        elif cpu_arch == "arm":
            release_type = "linux_aarch64"
    else:
        raise ValueError(f"Unrecognised OS: {os_type}")

    return [
        GccInfo(
            files=gcc_releases[release_name][release_type],
            release_name=release_name,
            os_arch=release_type,
        )
    ]


def download_toolchain(file_url: str, save_path: Path = Path.cwd()) -> Path:
    """
    Download the toolchain from the given URL into the given path.
    Displays a progress bar in the terminal.

    :param file_url: URL to download the toolchain from.
    :param save_path: Path to save the downloaded file.
    :return: Full path to the downloaded file.
    """
    print(f"Downloading toolchain from:\n\t{file_url}")
    if not save_path.is_dir():
        raise FileNotFoundError(f"Toolchain save path not found: {save_path}")
    url_file_name = os.path.basename(file_url)
    file_path = save_path / url_file_name
    print(f"Into: ./{Path(file_path).absolute().relative_to(Path.cwd())}")
    if file_path.is_file():
        raise FileExistsError(f"Toolchain file already exists: {file_path}")

    response = urllib.request.urlopen(file_url)
    total_length = int(response.getheader("Content-Length"))
    chunk_size = 8192

    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )
    task_id = progress.add_task("Downloading...", total=total_length)
    with progress, open(file_path, "wb") as out_file:
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            progress.update(task_id, advance=len(chunk))
    return file_path


def uncompress_toolchain(file_path: Path, destination: Path = Path.cwd()) -> Path:
    """
    Uncompress the given compressed file into the provided directory.

    Current extensions supported:
    - .zip
    - .tar.bz2
    - .tar.xz

    :param file_path: Path to the file to uncompress.
    :param destination: Path to uncompress the file into.
    :return: Full path to the uncompressed directory.
    """
    print(f"\nUncompressing toolchain file: ./{file_path.relative_to(Path.cwd())}")
    print(f"Into: {destination.resolve().relative_to(Path.cwd())}/")
    if not destination.is_dir():
        raise FileNotFoundError(f"Destination directory not found: {destination}")
    if not file_path.is_file():
        raise FileNotFoundError(f"File to uncompress not found: {file_path}")
    # The uncompressed folder will start with the same two words
    # (separated by '-') as the compressed file, or arm_none_eabi_gcc_toolchain
    uncompressed_folder_start = (
        str((destination / file_path.stem.split("-")[0]).resolve()),
        str((destination / "gcc-arm-none-eabi-").resolve()),
        str((destination / "arm_none_eabi_gcc_").resolve()),
    )
    for item in destination.iterdir():
        item = item.resolve()
        if str(item).startswith(uncompressed_folder_start):
            raise FileExistsError(
                f"Uncompressed folder already exists: {os.path.join(destination, item)}"
            )

    if str(file_path).endswith(".zip"):
        # Special case the 9-2020-q2 and 9-2019-q4 windows zip because they don't have a top folder
        bad_zip_filename1 = os.path.basename(gcc_releases["9-2020-q2"]["win32"]["url"])
        bad_zip_filename2 = os.path.basename(gcc_releases["9-2019-q4"]["win32"]["url"])
        if str(file_path).endswith(bad_zip_filename1):
            final_destination = destination / bad_zip_filename1.replace(".zip", "")
            final_destination.mkdir(exist_ok=False)
        elif str(file_path).endswith(bad_zip_filename2):
            final_destination = destination / bad_zip_filename2.replace(".zip", "")
            final_destination.mkdir(exist_ok=False)
        else:
            final_destination = destination
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(path=final_destination)

    elif str(file_path).endswith(".tar.bz2"):
        with tarfile.open(file_path, "r:bz2") as tar_ref:
            tar_ref.extractall(path=destination)

    elif str(file_path).endswith(".tar.xz"):
        with tarfile.open(file_path, "r:xz") as tar_ref:
            tar_ref.extractall(path=destination)

    else:
        raise ValueError(f"Unsupported file extension: {file_path}")

    # Get the full name of the uncompressed folder
    for item in destination.iterdir():
        item = item.resolve()
        if str(item).startswith(uncompressed_folder_start):
            return item
    raise FileNotFoundError(
        f"Uncompressed folder not found with this start path: {uncompressed_folder_start}"
    )


def generate_package_version(gcc_release_name: str) -> str:
    """
    Generate a package version based on the GCC release and this package version.

    :param gcc_release: GCC release name.
    :return: Combined package version string.
    """
    return gcc_short_versions[gcc_release_name] + "." + package_builder_version


def create_package_files(
    package_path: Path, gcc_path: Path, package_version: str
) -> None:
    """
    Create the package files with the provided GCC toolchain folder and
    script launchers for each executable.

    :param package_path: Path to the package directory.
    :param gcc_folder: Path to the GCC toolchain folder.
    """
    package_path = package_path.resolve()
    gcc_path = gcc_path.resolve()
    print(f"\nCreating package files in: {package_path.relative_to(Path.cwd())}")
    if not package_path.is_dir():
        raise FileNotFoundError(f"Package directory not found: {package_path}")
    if not gcc_path.is_dir():
        raise FileNotFoundError(f"GCC toolchain folder not found: {gcc_path}")
    # Check gcc_path is inside package_path
    if not os.path.commonpath([package_path, gcc_path]) == str(package_path):
        raise ValueError(
            f"GCC toolchain folder not inside the package path: {gcc_path}"
        )

    # Ensure the gcc_folder is a relative path to the package_path
    gcc_folder = gcc_path.relative_to(package_path)

    # Iterate through all the bin files to figure out which executables are available
    bin_files = []
    print("Found executables:")
    for root, _, files in os.walk(gcc_path / "bin"):
        for file in files:
            bin_file = os.path.basename(file)
            if bin_file.startswith("arm-none-eabi-"):
                func_name = bin_file.replace("arm-none-eabi-", "run_")
            else:
                func_name = "run_" + bin_file
            func_name = func_name.replace(".exe", "")
            func_name = re.sub("[^0-9a-zA-Z_]", "_", func_name)
            bin_files.append((bin_file, func_name))
            print(f"- {bin_file} ({func_name}.py)")
    if not bin_files:
        raise FileNotFoundError("No executables found in the GCC toolchain bin folder")

    # Create a python file per executable to launch it
    for bin_file, func_name in bin_files:
        with open(package_path / f"{func_name}.py", "w") as file:
            file.write(
                file_templates.executable_launcher.format(
                    bin=bin_file, func_name=func_name, gcc_folder=gcc_folder
                )
            )

    # Create the package pyproject.toml file
    pyproject_scripts = []
    for bin_file, func_name in bin_files:
        pyproject_scripts.append(
            f'"{bin_file.replace(".exe", "")}" = "{PACKAGE_NAME}.{func_name}:{func_name}"'
        )
    with open(package_path.parents[1] / "pyproject.toml", "w") as file:
        file.write(
            file_templates.pyproject_toml.format(
                version=package_version, bin_scripts="\n".join(pyproject_scripts)
            )
        )

    # Create the MANIFEST.in file
    with open(package_path.parents[1] / "MANIFEST.in", "w") as file:
        file.write(file_templates.manifest_in.format(gcc_folder=gcc_folder))


def build_python_wheel(package_path: Path, wheel_dir: Path, wheel_plat: str) -> None:
    """
    Create a Python wheel from the package directory.

    :param package_path: Path to the package directory.
    :return: Path to the created wheel file.
    """
    print(f"\nCreating Python wheel from: {package_path.relative_to(Path.cwd())}")
    if not package_path.is_dir():
        raise FileNotFoundError(f"Package directory not found: {package_path}")

    # Generate the expected wheel file name from the pyproject.toml
    with open(package_path / "pyproject.toml", "rb") as file:
        pyproject_toml = tomli.load(file)
    project_name = pyproject_toml["project"]["name"].replace("-", "_")
    project_version = pyproject_toml["project"]["version"]
    wheel_path = wheel_dir / f"{project_name}-{project_version}-py3-none-any.whl"
    if wheel_path.is_file():
        raise FileExistsError(
            f"Wheel file about to be created already exists: {wheel_path}"
        )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--wheel-dir",
            wheel_dir,
            ".",
        ],
        check=True,
        cwd=package_path,
    )

    if not wheel_path.is_file():
        raise FileNotFoundError(f"Wheel file not created: {wheel_path}")

    new_wheel_path = (
        wheel_dir / f"{project_name}-{project_version}-py3-none-{wheel_plat}.whl"
    )
    if new_wheel_path.is_file():
        raise FileExistsError(
            f"Wheel file with the platform tag already exists: {new_wheel_path}"
        )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "wheel",
            "tags",
            "--platform-tag",
            wheel_plat,
            wheel_path.name,
        ],
        check=True,
        cwd=wheel_dir,
    )
    wheel_path.unlink()

    if not new_wheel_path.is_file():
        raise FileNotFoundError(
            f"Wheel file with the platform tag not created: {new_wheel_path}"
        )

    return new_wheel_path


def create_sha256_hash(file_path: Path) -> str:
    """
    Create a SHA256 hash file for the given file in the same directory.

    :param file_path: Path to the file to hash.
    :return: SHA256 hash file path.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    sha256_file_path = file_path.with_suffix(".sha256")
    with open(sha256_file_path, "w") as file:
        file.write(f"{sha256_hash.hexdigest()} {file_path.name}\n")
    return sha256_file_path


def build_package_for_local_machine() -> None:
    print(f"Project directory: {PROJECT_PATH.relative_to(Path.cwd())}")
    if not PROJECT_PATH.is_dir() or not PACKAGE_PATH.is_dir():
        raise FileNotFoundError(
            f"Project/Package directory not found:\n\t{PROJECT_PATH}\n\t{PACKAGE_PATH}"
        )

    gcc_releases_list = get_gcc_releases()
    for gcc_release in gcc_releases_list:
        print(f"GCC release: {gcc_release.release_name} ({gcc_release.arch})\n")

        gcc_zip_file = download_toolchain(gcc_release.files["url"])
        gcc_path = uncompress_toolchain(gcc_zip_file, PACKAGE_PATH)
        create_package_files(
            PACKAGE_PATH,
            gcc_path,
            generate_package_version(gcc_release.release_name),
        )
        wheel_path = build_python_wheel(
            PROJECT_PATH, PROJECT_PATH / "dist", gcc_release.files["wheel_plat"]
        )
        create_sha256_hash(wheel_path)


if __name__ == "__main__":
    build_package_for_local_machine()
    sys.exit(0)
