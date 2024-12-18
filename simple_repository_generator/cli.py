#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

try:
    from simple_repository_generator.repo_gen import generate_simple_repository
except ImportError:
    # This is a bit of a hack, when running as a script, the package_builder
    # module is not available, so add the directory to the sys.path
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from simple_repository_generator.repo_gen import generate_simple_repository


app = typer.Typer()
THIS_PROJECT_ROOT = Path(__file__).resolve().parents[0]
DEFAULT_OUTPUT_PATH = (THIS_PROJECT_ROOT / ".." / "simple_repository_static").resolve()


@app.command()
def generate(
    repo: str,
    output: Annotated[Optional[Path], typer.Option()] = DEFAULT_OUTPUT_PATH,
    overwrite: bool = True,
):
    """
    Generate a simple repository from wheels found in a GH repository Releases.

    :param repo: The GitHub repository to generate the repository from.
    :param overwrite: Overwrite the output folder if it exists.
    """
    print(f"Generating simple repository from GH Releases in: {repo}")
    if not overwrite and output.exists():
        raise FileExistsError(
            f"Output path {output} already exists, use --overwrite to overwrite it."
        )
    print(f"Output path: {output.relative_to(Path.cwd())}")
    generate_simple_repository(repo, output)


def main():
    app()


if __name__ == "__main__":
    main()
