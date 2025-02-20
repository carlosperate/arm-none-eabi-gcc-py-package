"""
This script gets the latest versions of this package for each GCC release,
and checks if they are all available in the provided Python package repository.
"""
import sys
import json
import subprocess


def get_package_versions():
    """
    Run the `python tools.py package-gcc-versions` command and parse the output
    as a Python list.
    """
    output = subprocess.run(
        ["python", "tools.py", "package-versions"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    print("Output for 'python tools.py package-versions':")
    print(output.stdout)
    return json.loads(output.stdout.decode())


def get_pip_available_versions(extra_index_url):
    """
    Run the `pip index versions arm-none-eabi-gcc-toolchain ...` command
    and return a string with the versions listed.
    """
    output = subprocess.run(
        [
            "pip", "index", "versions",
            "arm-none-eabi-gcc-toolchain",
            f"--index-url={extra_index_url}",
            "--disable-pip-version-check",
         ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    print("\nOutput for 'pip index versions arm-none-eabi-gcc-toolchain ...':")
    print(output.stdout)
    pip_output_lines = output.stdout.decode().splitlines()
    line_start = "Available versions: "
    for line in pip_output_lines:
        if line.startswith(line_start):
            return line[len(line_start):]
    raise ValueError("Could not find the available versions in the pip output.")


def check_all_package_versions_in_python_repository(extra_index_url):
    package_versions = get_package_versions()
    pip_output = get_pip_available_versions(extra_index_url)
    for package_version in package_versions:
        if package_version not in pip_output:
            raise ValueError(f"Package version '{package_version}' not found in the Python repository.")


def main():
    # Take a single command line argument, the pip extra index URL
    if len(sys.argv) != 2:
        raise ValueError("Need the pip extra index URL as a single argument.")
    extra_index_url = sys.argv[1]
    check_all_package_versions_in_python_repository(extra_index_url)
    print("\nAll package versions are available in the Python repository.")


if __name__ == "__main__":
    main()
