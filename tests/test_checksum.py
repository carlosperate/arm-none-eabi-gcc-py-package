"""Tests for the release archive checksum verification in package_creator."""
import hashlib

import pytest

from tools_src.package_creator import verify_checksum


@pytest.fixture
def archive(tmp_path):
    path = tmp_path / "toolchain.tar.xz"
    path.write_bytes(b"not really a toolchain")
    return path


def digest(path, algorithm):
    return hashlib.new(algorithm, path.read_bytes()).hexdigest()


def test_sha256_is_preferred_over_md5(archive):
    checksums = {"sha256": digest(archive, "sha256"), "md5": "0" * 32}

    assert verify_checksum(archive, checksums) == "sha256"


def test_md5_is_used_when_it_is_all_there_is(archive):
    assert verify_checksum(archive, {"md5": digest(archive, "md5")}) == "md5"


def test_uppercase_digest_is_accepted(archive):
    checksums = {"sha256": digest(archive, "sha256").upper()}

    assert verify_checksum(archive, checksums) == "sha256"


def test_mismatch_raises(archive):
    with pytest.raises(ValueError, match="mismatch"):
        verify_checksum(archive, {"sha256": "0" * 64})


def test_no_recorded_checksum_is_refused(archive):
    with pytest.raises(ValueError, match="No sha256 or md5"):
        verify_checksum(archive, {"url": "https://example.invalid/toolchain.tar.xz"})
