#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import shutil
import itertools
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated
from rich import print

try:
    from package_builder import package_creator as pc
except ImportError:
    # This is a bit of a hack, when running as a script, the package_builder
    # module is not available, so add the directory to the sys.path
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))

from package_builder import package_creator as pc
from package_builder.package_creator import (
    PROJECT_NAME,
    PROJECT_PATH,
    PACKAGE_NAME,
    PACKAGE_PATH,
)


app = typer.Typer()
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@app.command()
def clean():
    """
    Cleans the project from any build artifacts.
    """
    print("[green]Cleaning project[/green]")
    files = [
        PROJECT_ROOT / PROJECT_NAME / "MANIFEST.in",
        PROJECT_ROOT / PROJECT_NAME / "pyproject.toml",
    ]
    folders = [
        PROJECT_ROOT / ".mypy_cache",
        PROJECT_ROOT / PROJECT_NAME / "build",
        PROJECT_ROOT / PROJECT_NAME / "src" / f"{PACKAGE_NAME}.egg-info",
        PROJECT_ROOT / PROJECT_NAME / "build",
    ]

    print("\nDeleting explicitly files and folders...")
    for file in files:
        if file.exists():
            file.unlink()
            print(f"\tDeleted file: {file.relative_to(PROJECT_ROOT)}")
    for folder in folders:
        if folder.exists():
            shutil.rmtree(folder)
            print(f"\tDeleted folder: {folder.relative_to(PROJECT_ROOT)}")

    # All autogenerated "run_*.py" files
    print("\nFinding run_*.py files...")
    for run_file in (PACKAGE_PATH).rglob("run_*.py"):
        run_file.unlink()
        print(f"\tDeleted file: {run_file.relative_to(PROJECT_ROOT)}")

    # Find all __pycache__ folders and delete them, excluding directories starting with a dot
    print("\nFinding __pycache__ folders...")
    for folder in PROJECT_ROOT.rglob("__pycache__"):
        if not folder.relative_to(PROJECT_ROOT).parts[0].startswith("."):
            shutil.rmtree(folder)
            print(f"\tDeleted folder: {folder.relative_to(PROJECT_ROOT)}")

    # Find any GCC folders or compressed files and delete them
    print("\nFinding GCC folders and compressed files...")
    gcc_files = itertools.chain(
        PROJECT_ROOT.rglob("gcc-arm-*"),
        PROJECT_ROOT.rglob("arm-gnu-toolchain*"),
        PACKAGE_PATH.rglob("arm_none_eabi_*"),
    )
    for file in gcc_files:
        # Don't delete files or folders in dot directories
        if file.relative_to(PROJECT_ROOT).parts[0].startswith("."):
            continue
        # Delete compressed files
        if file.is_file() and str(file).endswith((".zip", ".tar.bz2", ".tar.xz")):
            file.unlink()
            print(f"\tDeleted file: {file.relative_to(PROJECT_ROOT)}")
        # Delete folders that start with these names
        elif file.is_dir():
            shutil.rmtree(file)
            print(f"\tDeleted folder: {file.relative_to(PROJECT_ROOT)}")

    print("\nCleaning done!")


@app.command()
def build(
    release: Annotated[Optional[str], typer.Option(help="GCC release name")] = None,
    os: Annotated[Optional[str], typer.Option(help="Operating System name")] = None,
    arch: Annotated[Optional[str], typer.Option(help="CPU architecture")] = None,
):
    """
    Builds the Python package with the selected GCC release.

    If os and arch are set to "all", it will built packages for all the release platforms.
    """
    print("\n[green]Start building Python package/s[/green]")

    print(f"Package directory: {PROJECT_PATH.relative_to(Path.cwd())}\n")
    if not PROJECT_PATH.is_dir() or not PACKAGE_PATH.is_dir():
        raise FileNotFoundError(
            f"Project/Package directory not found:\n\t{PROJECT_PATH}\n\t{PACKAGE_PATH}"
        )

    selected_gcc_releases = pc.get_gcc_releases(release, os, arch)
    for gcc_release in selected_gcc_releases:
        # Perform a clean build for each release
        clean()

        release_name = f"{gcc_release.release_name} ({gcc_release.os_arch}"
        print(f"\n[green]Building GCC release: {release_name})[/green]")

        # Get the GCC release and uncompress it in the package directory
        print("\n[green]Downloading and uncompressing GCC toolchain[/green]")
        gcc_zip_file = pc.download_toolchain(gcc_release.files["url"])
        gcc_path = pc.uncompress_toolchain(gcc_zip_file, PACKAGE_PATH)

        # Create the package files with the GCC toolchain folder inside
        print("\n[green]Creating Python package files[/green]")
        package_version = pc.generate_package_version(gcc_release.release_name)
        pc.create_package_files(PACKAGE_PATH, gcc_path, package_version)

        print("\n[green]Building Python wheel[/green]")
        dist_folder = PROJECT_ROOT / "dist"
        dist_folder.mkdir(exist_ok=True)
        wheel_path = pc.build_python_wheel(
            PROJECT_PATH, dist_folder, gcc_release.files["wheel_plat"]
        )
        pc.create_sha256_hash(wheel_path)

        print(f"\n[green]Package {release_name}) created![/green]\n")


@app.command()
def get_package_version(gcc_release_name: str):
    """
    Get the package version string for the specified GCC release.
    """
    # Check the release name exists (all releases have win version), but ignore result
    _ = pc.get_gcc_releases(gcc_release_name, "win", "x86_64")
    package_version = pc.generate_package_version(gcc_release_name)
    print(f"{package_version}")


def main():
    app()


if __name__ == "__main__":
    main()
