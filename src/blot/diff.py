"""Turn `git diff` output into per-file added and removed lines with line numbers."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from blot.git import run_git

_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
_TRAILING_COMMENT = re.compile(r"\s+(?:#|//)\s.*$")
_TRIVIAL = re.compile(r"^(?:[\s{}()\[\];,.:]*|(?:import|from|#include|using|package|require)\b.*|(?:return|pass|break|continue|else|end|try|finally)\b\W*)$")


def normalize_line(text: str) -> str:
    """Collapse whitespace and drop trailing comments so cosmetic edits still match."""
    return " ".join(_TRAILING_COMMENT.sub("", text).split())


def is_trivial_line(normalized: str) -> bool:
    """Lines too generic to mean anything on their own: brackets, imports, bare keywords."""
    return len(normalized) < 12 or bool(_TRIVIAL.match(normalized))


def line_hash(normalized: str) -> str:
    return hashlib.blake2b(normalized.encode("utf-8"), digest_size=8).hexdigest()


@dataclass
class FileChange:
    path: str  # path after the change (old path for deleted files)
    old_path: str | None  # path before the change (None for new files)
    removed: list[tuple[int, str]] = field(default_factory=list)  # (old line number, text)
    added: list[tuple[int, str]] = field(default_factory=list)  # (new line number, text)


def parse_unified_diff(text: str) -> list[FileChange]:
    """Parse `git diff -U0` output. Binary files and mode-only changes produce no lines."""
    changes: list[FileChange] = []
    current: FileChange | None = None
    old_path: str | None = None
    old_no = new_no = 0
    for line in text.splitlines():
        if line.startswith("--- "):
            old_path = None if line == "--- /dev/null" else line[6:]  # strip "--- a/"
        elif line.startswith("+++ "):
            new_path = old_path if line == "+++ /dev/null" else line[6:]  # strip "+++ b/"
            current = FileChange(path=new_path or "", old_path=old_path)
            changes.append(current)
        elif current is None:
            continue
        elif m := _HUNK.match(line):
            old_no, new_no = int(m.group(1)), int(m.group(3))
        elif line.startswith("-"):
            current.removed.append((old_no, line[1:]))
            old_no += 1
        elif line.startswith("+"):
            current.added.append((new_no, line[1:]))
            new_no += 1
    return changes


def read_changes(repo: str, rev_range: str | None = None) -> list[FileChange]:
    """Staged changes by default, or the changes in a commit range like `origin/main..HEAD`."""
    args = ["diff", "-U0", "--no-color", "--no-ext-diff", "-M"]
    args.append(rev_range if rev_range else "--cached")
    return parse_unified_diff(run_git(repo, *args))
