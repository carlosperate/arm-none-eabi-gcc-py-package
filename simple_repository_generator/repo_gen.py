#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import sys
import hashlib
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

import requests
from github import Github
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn

# A bit of a hack, ensure the git repo root is in the PATH to be able to reach the package_builder module
sys.path.append(str(Path(__file__).resolve().parents[1]))

from package_builder.package_creator import PROJECT_NAME


@dataclass
class WheelData:
    name: str
    url: str
    sha256: str
    python_requires: str = "&gt;=3.6"  # Default to Python 3.6+


def normalise_project_name(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def get_gh_releases_wheel_urls(
    repo_name: str, token=None
) -> Dict[str, List[WheelData]]:
    """Get wheel URLs from GitHub Releases."""
    gh = Github(token) if token else Github()
    repo = gh.get_repo(repo_name)
    wheel_files = {}
    for release in repo.get_releases():
        wheel_files[release.tag_name] = []
        release_assets = list(release.get_assets())
        for asset_wheel in release_assets:
            if not asset_wheel.name.endswith(".whl"):
                continue
            print(f"\n\tFound wheel: {asset_wheel.name}")
            # Use the sha256 file in the assets, or calculate it if not present
            # We don't expect more than 10-20 assets, so fine to iterate again
            sha256_hash = None
            for asset_sha in release_assets:
                if asset_sha.name != f"{asset_wheel.name}.sha256":
                    continue
                # This file will be in the format "<sha256 hash> filename.whl\n"
                with requests.get(asset_sha.browser_download_url) as r:
                    sha256_file_contents = r.text.strip()
                if asset_wheel.name in sha256_file_contents:
                    sha256_hash = sha256_file_contents.split()[0]
                    if len(sha256_hash) != 64:
                        sha256_hash = None
                        print(f"\tInvalid SHA-256 in {asset_sha.browser_download_url}:")
                        print(sha256_file_contents)
                    else:
                        print(f"\tFound SHA-256 ({sha256_hash}) in\n\t{asset_sha.name}")
                break
            else:
                print(f"\tCouldn't find matching SHA-256 file for {asset_wheel.name}")
            if sha256_hash is None:
                sha256_hash = calculate_sha256(asset_wheel.browser_download_url)

            wheel_files[release.tag_name].append(
                WheelData(
                    name=asset_wheel.name,
                    url=asset_wheel.browser_download_url,
                    sha256=sha256_hash,
                )
            )
    return wheel_files


def calculate_sha256(url: str) -> str:
    """Calculates the SHA-256 hash of a file available at the given URL."""

    def _calculate_sha256(url: str) -> str:
        sha256_hash = hashlib.sha256()
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        chunk_size = 8192

        print(f"\tDownloading & hashing: {url.split('/')[-1]}")
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            DownloadColumn(),
            TransferSpeedColumn(),
        ) as progress:
            task = progress.add_task(f"{' ' * 12}", total=total_size)
            for chunk in response.iter_content(chunk_size=chunk_size):
                sha256_hash.update(chunk)
                progress.update(task, advance=len(chunk))

        return sha256_hash.hexdigest()

    for i in range(1, 4):
        try:
            return _calculate_sha256(url)
        except requests.exceptions.ConnectionError:
            print(f"\tFailed attempt {i} to download file at {url}.")
            if i == 3:
                raise
            else:
                print("\tRetrying...")


def gen_repo_html(packages: Dict[str, Dict[str, List[WheelData]]], output: Path) -> str:
    """Generate HTML files for the simple repository."""
    output.mkdir(parents=True, exist_ok=False)

    # Generate root index.html with links to each package
    package_links = []
    for package in packages:
        package_name = normalise_project_name(package)
        href = f"{package_name}/"
        package_links.append(f'<a href="{href}">{package_name}</a>')
    with open(output / "index.html", "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n")
        f.write("<head>\n")
        f.write('\t<meta name="pypi:repository-version" content="1.0">\n')
        f.write('\t<title>Simple Index</title>\n\t<meta charset="UTF-8" />\n')
        f.write("</head>\n")
        f.write("<body>\n\t")
        f.write("\n\t".join(package_links))
        f.write("\n</body>\n</html>\n")

    # Generate file pages
    for package in packages:
        package_name = normalise_project_name(package)
        version_links = []
        for version, wheels in packages[package].items():
            for wheel in wheels:
                href = f"{wheel.url}#sha256={wheel.sha256}"
                version_links.append(
                    f'<a href="{href}" data-requires-python="{wheel.python_requires}">{wheel.name}</a>'
                )
        package_path = output / f"{package_name}"
        package_path.mkdir(parents=False, exist_ok=True)
        with open(package_path / "index.html", "w") as f:
            title = f"Links for {package_name}"
            f.write(f"<!DOCTYPE html>\n<html>\n")
            f.write("<head>\n")
            f.write('\t<meta name="pypi:repository-version" content="1.0">\n')
            f.write(f'\t<title>{title}</title>\n\t<meta charset="UTF-8" />\n')
            f.write("</head>\n")
            f.write("<body>\n\t")
            f.write(f"<h1>{title}</h1>\n\t")
            f.write("<br />\n\t".join(version_links))
            f.write("\n</body>\n</html>\n")


def generate_simple_repository(repo: str, output: Path) -> None:
    print(f"Getting wheel URLs from GH Releases in: {repo}")
    releases_wheels = get_gh_releases_wheel_urls(repo)
    print("\tDone.\n")
    print(f"Generating HTML file in: {output}")
    gen_repo_html({PROJECT_NAME: releases_wheels}, output)
    print("\tDone.")
