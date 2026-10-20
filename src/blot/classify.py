"""Decide what kind of commit something is. Most of Blot's precision comes from here.

Fix severity:
    0  not a fix (feature, docs, chore)
    1  routine fix ("fix typo", "fix lint", a bare "fix stuff")
    2  load-bearing fix: a fix verb pointing at an issue ("fixes #12"), or a commit that names
       a real defect (crash, leak, race, regression, CVE, injection, deadlock, data loss, ...)

`is_refactor` flags commits that move code without changing what it does (file splits,
renames, mass reformatting). When blame lands on one of these, Blot traces further
back. That is how it finds the 2020 Flask fix behind the 2023 "Split the App..." commit.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class CommitInfo:
    sha: str
    subject: str
    body: str
    files_changed: int
    lines_added: int
    lines_removed: int
    renames: int


_ISSUE = r"(?:#\d+|gh-\d+|[A-Z][A-Z0-9]+-\d+)"
# "fixes #12" means the commit is the fix; "closes #12" is often just housekeeping.
_FIX_ISSUE = re.compile(rf"\b(?:fix(?:e[sd])?|resolve[sd]?)\b[:\s]+{_ISSUE}", re.IGNORECASE)
_ANY_ISSUE = re.compile(rf"(?<![\w/]){_ISSUE}\b")
_FIX_WORD = re.compile(r"\b(?:fix(?:e[sd]|ing)?|bug(?:fix)?|hotfix|patch(?:e[sd])?|repair(?:e[sd])?|workaround)\b", re.IGNORECASE)
# Strong defect words make a commit load-bearing on their own; weak ones need a fix verb too.
_DEFECT = re.compile(
    r"\b(?:crash(?:e[sd])?|segfault|panic|leak(?:s|ing)?|race(?: condition)?|deadlock|regression|"
    r"cve-\d{4}-\d+|vulnerab\w*|injection|xss|csrf|ssrf|overflow|underflow|corrupt\w*|"
    r"data loss|infinite loop|null pointer|use-after-free|reference cycle|off-by-one)\b",
    re.IGNORECASE,
)
_WEAK_DEFECT = re.compile(r"\b(?:hang(?:s|ing)?|timeout|broken|incorrect(?:ly)?|wrong|security)\b", re.IGNORECASE)
_ROUTINE = re.compile(
    r"\b(?:typo|typos|lint|linter|flake8|pylint|mypy|ruff|eslint|format(?:ting)?|style|"
    r"whitespace|spelling|docs?|document\w*|docstring|comment|readme|changelog|warning|ci|build|"
    r"examples?|tutorial|tests?|testing|translation|note|mention\w*|advice|wording|sentence|links?|gramma\w*)\b",
    re.IGNORECASE,
)
_REFACTOR = re.compile(
    r"\b(?:move[sd]?|moving|split|splits|splitting|rename[sd]?|renaming|reorganiz\w*|"
    r"restructur\w*|refactor\w*|reformat\w*|extract(?:ed)?|black|prettier|isort|clang-format)\b",
    re.IGNORECASE,
)


def fix_severity(commit: CommitInfo, issue_labels: list[str] | None = None) -> int:
    subject, text = commit.subject, f"{commit.subject}\n{commit.body}"
    if issue_labels and any("bug" in label.lower() or "security" in label.lower() for label in issue_labels):
        return 2
    fixish = bool(_FIX_WORD.search(subject) or _FIX_ISSUE.search(text))
    if _ROUTINE.search(subject):  # docs/tests/style work, even when it mentions a defect word
        return 1 if fixish else 0
    if _DEFECT.search(subject):
        return 2
    if _FIX_ISSUE.search(text) or (_WEAK_DEFECT.search(subject) and _FIX_WORD.search(subject)):
        return 2
    return 1 if fixish else 0


def is_refactor(commit: CommitInfo) -> bool:
    if _FIX_WORD.search(commit.subject) or _DEFECT.search(commit.subject):
        return False
    if _REFACTOR.search(commit.subject):
        return True
    if commit.files_changed and commit.renames * 2 >= commit.files_changed:
        return True
    big = min(commit.lines_added, commit.lines_removed) >= 50
    balanced = abs(commit.lines_added - commit.lines_removed) <= 0.1 * max(commit.lines_added, commit.lines_removed, 1)
    return big and balanced


def linked_issues(commit: CommitInfo) -> list[str]:
    """Issue references in the message, in order, without duplicates."""
    seen: dict[str, None] = {}
    for ref in _ANY_ISSUE.findall(f"{commit.subject}\n{commit.body}"):
        seen.setdefault(ref, None)
    return list(seen)
