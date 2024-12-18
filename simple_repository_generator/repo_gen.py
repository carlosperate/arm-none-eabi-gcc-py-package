#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List
from collections import namedtuple

import requests
from github import Github
from rich.progress import Progress


WheelURl = namedtuple("Wheel", ["name", "url", "sha256"])


def get_gh_releases_wheel_urls(repo_name: str, token=None) -> Dict[str, List[WheelURl]]:
    """Get wheel URLs from GitHub Releases."""
    gh = Github(token) if token else Github()
    repo = gh.get_repo(repo_name)
    wheel_files = {}
    for release in repo.get_releases():
        wheel_files[release.tag_name] = []
        for asset in release.get_assets():
            if asset.name.endswith(".whl"):
                wheel_files[release.tag_name].append(
                    WheelURl(
                        name=asset.name,
                        url=asset.browser_download_url,
                        sha256=calculate_sha256(asset.browser_download_url),
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
        with Progress() as progress:
            task = progress.add_task(f"\t\t{(total_size/(1024*1024)):.2f} MB ", total=total_size)
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


def gen_repo_html(packages: Dict[str, Dict[str, List[WheelURl]]], output: Path) -> str:
    """Generate HTML files for the simple repository."""
    if output.exists():
        if not output.is_dir():
            raise NotADirectoryError(f"Output path '{output}' is not a directory.")
        else:
            shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=False)

    # Generate root index.html with links to each package
    package_links = []
    for package in packages:
        href = f"{package}/"
        package_links.append(f'<a href="{href}">{package}</a>')
    with open(output / "index.html", "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n")
        f.write("<head>\n")
        f.write('\t<title>Simple Index</title>\n\t<meta charset="UTF-8" />\n')
        f.write("</head>\n")
        f.write("<body>\n\t")
        f.write("\n\t".join(package_links))
        f.write("\n</body>\n</html>")

    # Generate file pages
    for package in packages:
        version_links = []
        for version, urls in packages[package].items():
            for wheel_url in urls:
                href = f"{wheel_url.url}#sha256={wheel_url.sha256}"
                version_links.append(f'<a href="{href}">{wheel_url.name}</a>')
        package_path = output / f"{package}"
        package_path.mkdir(parents=False, exist_ok=True)
        with open(package_path / "index.html", "w") as f:
            title = f"Links for {package}"
            f.write(f"<!DOCTYPE html>\n<html>\n")
            f.write("<head>\n")
            f.write(f'\t<title>{title}</title>\n\t<meta charset="UTF-8" />\n')
            f.write("</head>\n")
            f.write("<body>\n\t")
            f.write(f"<h1>{title}</h1>\n\t")
            f.write("<br />\n".join(version_links))
            f.write("\n</body>\n</html>")


def generate_simple_repository(repo: str, output: Path) -> None:
    print(f"Getting wheel URLs from GH Releases in: {repo}")
    releases_wheels = get_gh_releases_wheel_urls(repo)
    print("\tDone.\n")
    print(f"Generating HTML file in: {output}")
    gen_repo_html({"arm_none_eabi_gcc_toolchain": releases_wheels}, output)
    print("\tDone.")
