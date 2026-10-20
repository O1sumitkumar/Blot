"""Build or incrementally refresh the history index.

Steps:
    1. walk `git log --numstat -M` from the last indexed sha to HEAD
    2. classify each commit (classify.py), store severity and refactor flags
    3. for load-bearing fixes, hash the lines they removed   -> fix_removed_lines
    4. count file pairs changed together (skip huge commits) -> cochange
    5. with --github: map commits to PRs and linked issues via `gh api`
Targets: under 60 s for 50k commits on a laptop; incremental refresh under 1 s.
"""

from __future__ import annotations


def build_index(repo: str, full: bool = False, github: bool = False) -> None:
    raise NotImplementedError("TODO(M1): see module docstring")
