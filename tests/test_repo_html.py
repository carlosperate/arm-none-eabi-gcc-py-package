"""Tests for the simple repository HTML generation."""
from tools_src.simple_repository_generator import WheelData, gen_repo_html


def wheel(name, python_requires=""):
    return WheelData(
        name=name,
        url=f"https://example.invalid/{name}",
        sha256="a" * 64,
        metadata_url=f"https://example.invalid/{name}.metadata",
        metadata_sha256="b" * 64,
        python_requires=python_requires,
    )


def test_requires_python_comes_from_each_wheel(tmp_path):
    wheels = {
        "v14.2.1": [wheel("pkg-14.2.1-py3-none-any.whl", ">=3.8")],
        "v13.3.0": [wheel("pkg-13.3.0-py3-none-any.whl")],
    }
    gen_repo_html({"arm-none-eabi-gcc-toolchain": wheels}, tmp_path / "out")
    links = (tmp_path / "out" / "arm-none-eabi-gcc-toolchain" / "index.html").read_text().splitlines()

    new, old = (l for l in links if "14.2.1" in l), (l for l in links if "13.3.0" in l)
    assert 'data-requires-python="&gt;=3.8"' in next(new)
    assert "data-requires-python" not in next(old)
