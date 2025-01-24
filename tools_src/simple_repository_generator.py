#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import hashlib
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

import requests
from github import Github
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn

from tools_src.package_creator import PROJECT_NAME


@dataclass
class WheelData:
    name: str
    url: str
    sha256: str
    metadata_url: str = ""
    metadata_sha256: str = ""
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
            # Look for the respective metadata file and both sha256 files
            # We don't expect more than 10-20 assets, so fine to iterate again
            wheel_sha256 = None
            metadata_url = ""
            metadata_sha256 = ""
            for asset in release_assets:
                if asset.name == f"{asset_wheel.name}.sha256":
                    # This file will be in the format "<sha256 hash> filename.whl\n"
                    with requests.get(asset.browser_download_url) as r:
                        sha256_file_contents = r.text.strip()
                    if asset_wheel.name in sha256_file_contents:
                        wheel_sha256 = sha256_file_contents.split()[0]
                        if len(wheel_sha256) != 64:
                            raise ValueError(
                                f"Invalid SHA-256 in {asset.browser_download_url}: \n"
                                f"{sha256_file_contents}\n"
                                f"{wheel_sha256}"
                            )
                        print(f"\tFound wheel SHA-256 ({wheel_sha256}) in\n\t\t{asset.name}")
                elif asset.name == f"{asset_wheel.name}.metadata":
                    # Ensure the URL is the same as the wheel URL + ".metadata" extension
                    if (
                        asset.browser_download_url
                        != asset_wheel.browser_download_url + ".metadata"
                    ):
                        raise ValueError(
                            f"Metadata file URL doesn't match the wheel URL:\n"
                            f"\tWheel:    {asset_wheel.browser_download_url}\n"
                            f"\tMetadata: {asset.browser_download_url}"
                        )
                    metadata_url = asset.browser_download_url
                    print(f"\tFound metadata: {asset.name}")
                elif asset.name == f"{asset_wheel.name}.metadata.sha256":
                    with requests.get(asset.browser_download_url) as r:
                        metadata_sha256_file = r.text.strip()
                    metadata_sha256 = metadata_sha256_file.split()[0]
                    if len(metadata_sha256) != 64:
                        raise ValueError(
                            f"Invalid SHA-256 in {asset.browser_download_url}:\n"
                            f"{metadata_sha256_file}\n"
                            f"{metadata_sha256}"
                        )
                    print(
                        f"\tFound metadata SHA-256 ({metadata_sha256}) in\n\t\t{asset.name}"
                    )

            if not metadata_url and metadata_sha256:
                raise ValueError(
                    f"Metadata SHA-256 found without a metadata file for {asset_wheel.name}"
                )
            if metadata_url and not metadata_sha256:
                print(f"\tMetadata file found without a SHA-256 for {asset_wheel.name}")
                metadata_sha256 = calculate_sha256(metadata_url)
            if wheel_sha256 is None:
                print(f"\tCouldn't find matching SHA-256 for {asset_wheel.name}")
                wheel_sha256 = calculate_sha256(asset_wheel.browser_download_url)

            wheel_files[release.tag_name].append(
                WheelData(
                    name=asset_wheel.name,
                    url=asset_wheel.browser_download_url,
                    sha256=wheel_sha256,
                    metadata_url=metadata_url,
                    metadata_sha256=metadata_sha256,
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
                    f'<a href="{href}" data-requires-python="{wheel.python_requires}" '
                    f'data-dist-info-metadata="sha256={wheel.metadata_sha256}" '
                    f'data-core-metadata="sha256={wheel.metadata_sha256}">'
                    f"{wheel.name}</a>"
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
