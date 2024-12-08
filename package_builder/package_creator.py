import os
import re
import sys
import tarfile
import zipfile
import platform
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional

import toml
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


PACKAGE_NAME = "arm_none_eabi_gcc_toolchain"
PACKAGE_PATH = Path(__file__).resolve().parents[1] / PACKAGE_NAME
PACKAGE_SRC_PATH = PACKAGE_PATH / "src" / PACKAGE_NAME


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
    # (separated by '-') as the compressed file
    uncompressed_folder_start = str(
        (destination / file_path.stem.split("-")[0]).resolve()
    )
    for item in destination.iterdir():
        item = item.resolve()
        if str(item).startswith(uncompressed_folder_start):
            raise FileExistsError(
                f"Uncompressed folder already exists: {os.path.join(destination, item)}"
            )

    if str(file_path).endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(path=destination)
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


def generate_package_version(gcc_release: str) -> str:
    """
    Generate a package version based on the GCC release and this package version.

    :param gcc_release: GCC release name.
    :return: Combined package version string.
    """
    return gcc_short_versions[gcc_release] + "." + package_builder_version


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
            func_name = bin_file.replace("arm-none-eabi-", "run_")
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
            f'"{bin_file}" = "{PACKAGE_NAME}.{func_name}:{func_name}"'
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


def get_gcc_release(
    release_name: Optional[str], os_type: Optional[str], cpu_arch: Optional[str]
):
    # Set default values
    # Python dictionaries are now ordered, so the latest release is the first one
    if release_name is None:
        release_name = list(gcc_releases.keys())[0]
    if os_type is None:
        os_type = platform.system()
    os_type = os_type.lower()
    if cpu_arch is None:
        cpu_arch = platform.machine()
    cpu_arch = cpu_arch.lower()

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

    return gcc_releases[release_name][release_type], release_name, release_type


def build_python_wheel(package_path: Path, wheel_dir: Path, wheel_plat: str) -> None:
    """
    Create a Python wheel from the package directory.

    :param package_path: Path to the package directory.
    """
    print(f"\nCreating Python wheel from: {package_path.relative_to(Path.cwd())}")
    if not package_path.is_dir():
        raise FileNotFoundError(f"Package directory not found: {package_path}")

    # To later find the wheel we check for any new files added to the wheel directory
    initial_files = set(wheel_dir.iterdir())

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

    # Generate the expected wheel file name from the pyproject.toml
    with open(package_path / "pyproject.toml", "r") as file:
        pyproject_toml = toml.load(file)
    wheel_path = wheel_dir / f"{pyproject_toml['project']['name']}-{pyproject_toml['project']['version']}-py3-none-any.whl"
    if not wheel_path.is_file():
        raise FileNotFoundError(f"Wheel file not found in: {wheel_dir}")

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


def build_package(
    gcc_release_name: Optional[str] = None,
    os_type: Optional[str] = None,
    cpu_arch: Optional[str] = None,
) -> None:
    print(f"Package directory: {PACKAGE_PATH.relative_to(Path.cwd())}")
    if not PACKAGE_PATH.is_dir() or not PACKAGE_SRC_PATH.is_dir():
        raise FileNotFoundError(f"Package directory not found: {PACKAGE_SRC_PATH}")

    gcc_release, gcc_release_name, gcc_release_arch = get_gcc_release(
        gcc_release_name, os_type, cpu_arch
    )
    print(f"GCC release: {gcc_release_name} ({gcc_release_arch})\n")

    gcc_zip_file = download_toolchain(gcc_release["url"])
    gcc_path = uncompress_toolchain(gcc_zip_file, PACKAGE_SRC_PATH)
    create_package_files(
        PACKAGE_SRC_PATH, gcc_path, generate_package_version(gcc_release_name)
    )
    build_python_wheel(PACKAGE_PATH, PACKAGE_PATH / "dist", gcc_release["wheel_plat"])


if __name__ == "__main__":
    build_package()
    sys.exit(0)
