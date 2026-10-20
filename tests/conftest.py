"""Shared fixtures. `make_repo` builds a throwaway git repo with a scripted history."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout


@pytest.fixture
def make_repo(tmp_path: Path):
    """Usage: repo = make_repo([("feat: add x", {"a.py": "x = 1\n"}), ("fix: crash (fixes #1)", {...})])"""

    def _make(commits: list[tuple[str, dict[str, str]]]) -> Path:
        repo = tmp_path / "repo"
        repo.mkdir()
        _git(repo, "init", "-q", "-b", "main")
        _git(repo, "config", "user.email", "test@example.com")
        _git(repo, "config", "user.name", "Test")
        for message, files in commits:
            for name, content in files.items():
                path = repo / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            _git(repo, "add", "-A")
            _git(repo, "commit", "-q", "-m", message)
        return repo

    return _make
