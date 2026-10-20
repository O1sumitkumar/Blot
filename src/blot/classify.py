"""Decide what kind of commit something is. Most of blot's precision comes from here.

Fix severity:
    0  not a fix (feature, docs, chore)
    1  routine fix ("fix typo", "fix lint")
    2  load-bearing fix: closes a bug issue, or names a real defect
       (crash, leak, race, regression, CVE, injection, deadlock, data loss, ...)

`is_refactor` flags commits that move code without changing what it does (file splits,
renames, mass reformatting). When blame lands on one of these, blot traces further
back. That is how it finds the 2020 Flask fix behind the 2023 "Split the App..." commit.
"""

from __future__ import annotations

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


def fix_severity(commit: CommitInfo, issue_labels: list[str] | None = None) -> int:
    # TODO(M1): keyword tiers + issue-reference verbs ("fixes #12" vs "closes #12")
    #           + GitHub bug labels when indexed with --github
    raise NotImplementedError


def is_refactor(commit: CommitInfo) -> bool:
    # TODO(M2): message keywords (move, split, rename, reformat, black, prettier)
    #           + high rename ratio + added roughly equal to removed
    raise NotImplementedError
