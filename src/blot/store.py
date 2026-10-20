"""Local SQLite index stored at .git/blot.db. Never committed, never leaves the machine.

Planned tables:
    meta(key, value)                          schema version, last indexed sha
    commits(sha, date, subject, severity, is_refactor, pr, issues)
    fix_removed_lines(line_hash, path, sha)   normalized lines deleted by fix commits
    cochange(path_a, path_b, support, confidence)
"""

from __future__ import annotations

import os
import sqlite3

from blot.git import run_git

SCHEMA_VERSION = 1


class Store:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    @staticmethod
    def db_path(repo: str) -> str:
        git_dir = run_git(repo, "rev-parse", "--absolute-git-dir").strip()
        return os.path.join(git_dir, "blot.db")

    @classmethod
    def open(cls, repo: str) -> Store | None:
        """Return the index, or None if `blot index` has never been run."""
        path = cls.db_path(repo)
        if not os.path.exists(path):
            return None
        return cls(sqlite3.connect(path))

    # TODO(M1): create_schema(), commit lookups, line-hash lookups, co-change lookups
