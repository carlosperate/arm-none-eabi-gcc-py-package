import os
import re
import sys
import tarfile
import zipfile
import urllib.request

from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

from package_builder import gcc_releases, file_templates

PACKAGE_NAME = "arm_none_eabi_gcc_toolchain"


def download_toolchain(file_url, save_path="."):
    """
    Download the toolchain from the given URL into the given path.
    Displays a progress bar in the terminal.

    :param file_url: URL to download the toolchain from.
    :param save_path: Path to save the downloaded file.
    :return: Full path to the downloaded file.
    """
    print(f"Downloading toolchain from: {file_url}")
    if not os.path.isdir(save_path):
        raise FileNotFoundError(f"Toolchain save path not found: {save_path}")
    url_file_name = os.path.basename(file_url)
    file_path = os.path.join(save_path, url_file_name)
    print(f"Into: {os.path.relpath(file_path, os.getcwd())}")
    if os.path.isfile(file_path):
        # FIXME:
        #raise FileExistsError(f"Toolchain file already exists: {file_path}")
        print("SKIPPING")
        return os.path.abspath(file_path)

    response = urllib.request.urlopen(file_url)
    total_length = int(response.getheader('Content-Length'))
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
    with progress, open(file_path, 'wb') as out_file:
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            progress.update(task_id, advance=len(chunk))
    return file_path


def uncompress_toolchain(file_path, destination="."):
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
    print(f"Uncompressing toolchain file: {file_path}")
    print(f"Into: {os.path.relpath(destination, os.getcwd())}/")
    if not os.path.isdir(destination):
        raise FileNotFoundError(f"Destination directory not found: {destination}")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File to uncompress not found: {file_path}")
    # The uncompressed folder will start with the same two words
    # (separated by '-') as the compressed file
    uncompressed_folder_start = os.path.abspath(os.path.join(
        destination, "-".join(os.path.basename(file_path).split("-")[:2])
    ))
    for item in os.listdir(destination):
        item = os.path.abspath(os.path.join(destination, item))
        if item.startswith(uncompressed_folder_start):
            # FIXME:
            # raise FileExistsError(f"Uncompressed folder already exists: {os.path.join(destination, item)}")
            print("SKIPPING")
            return item

    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(path=destination)
    elif file_path.endswith(".tar.bz2"):
        with tarfile.open(file_path, "r:bz2") as tar_ref:
            tar_ref.extractall(path=destination)
    elif file_path.endswith(".tar.xz"):
        with tarfile.open(file_path, "r:xz") as tar_ref:
            tar_ref.extractall(path=destination)
    else:
        raise ValueError(f"Unsupported file extension: {file_path}")

    # Get the full name of the uncompressed folder
    for item in os.listdir(destination):
        item = os.path.abspath(os.path.join(destination, item))
        if item.startswith(uncompressed_folder_start):
            return item
    raise FileNotFoundError(f"Uncompressed folder not found with this start path: {uncompressed_folder_start}")


def create_package_files(package_path, gcc_folder):
    """
    Create the package files with the provided GCC toolchain folder.

    :param package_path: Path to the package directory.
    :param gcc_folder: Path to the GCC toolchain folder.
    """
    print(f"Creating package files in: {package_path}")
    if not os.path.isdir(package_path):
        raise FileNotFoundError(f"Package directory not found: {package_path}")
    if not os.path.isdir(gcc_folder):
        raise FileNotFoundError(f"GCC toolchain folder not found: {gcc_folder}")
    if not os.path.commonpath([package_path, gcc_folder]) == package_path:
        raise ValueError(f"GCC toolchain folder not inside the package path: {gcc_folder}")
    
    # Ensure the gcc_folder is a relative path to the package_path
    gcc_folder = os.path.relpath(gcc_folder, package_path)

    # Iterate through all the bin files to figure out which executables are available
    bin_files = []
    print("Found executables:")
    for root, _, files in os.walk(os.path.join(package_path, gcc_folder, "bin")):
        for file in files:
            bin_file = os.path.basename(file)
            bin_short = bin_file.replace("arm-none-eabi-", "")
            bin_short = re.sub('[^0-9a-zA-Z_]', '_', bin_short)
            bin_files.append((bin_file, bin_short))
            print(f"- {bin_file} ({bin_short})")

    # Create a python file per executable to launch it
    for bin_file, bin_short in bin_files:
        with open(os.path.join(package_path, f"{bin_short}.py"), "w") as file:
            file.write(file_templates.executable_launcher.format(
                bin=bin_file, bin_short=bin_short, gcc_folder=gcc_folder
            ))

    # Create the package pyproject file
    pyproject_scripts = []
    for bin_file, bin_short in bin_files:
        pyproject_scripts.append(f'"{bin_file}" = "{PACKAGE_NAME}.{bin_short}:launch_{bin_short}"')
    with open(os.path.join(package_path, "pyproject.toml"), "w") as file:
        file.write(file_templates.package_pyproject.format(
            pyproject_scripts="\n".join(pyproject_scripts),
            gcc_folder=gcc_folder
        ))


def main():
    # Find gcc toolchain package path from this file path
    src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    package_path = os.path.join(src_path, PACKAGE_NAME)
    if not os.path.isdir(package_path):
        raise FileNotFoundError(f"Package directory not found: {package_path}")
    print(f"Package directory: {os.path.relpath(package_path, os.getcwd())}")
    
    # Get the GCC release and uncompress it in the package directory
    gcc_url = gcc_releases.gcc_releases["13.3.Rel1"]["mac_x86_64"]["url"]
    gcc_zip_file = download_toolchain(gcc_url)
    try:
        gcc_folder = uncompress_toolchain(gcc_zip_file, package_path)
    finally:
        # FIXME:
        #os.remove(gcc_zip_file)
        pass

    # Create the package files with the GCC toolchain folder inside
    create_package_files(package_path, gcc_folder)



if __name__ == "__main__":
    sys.exit(main())
