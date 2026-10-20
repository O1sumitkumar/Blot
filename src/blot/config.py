"""Settings, read from `[tool.blot]` in pyproject.toml or a `.blot.toml` file."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Config:
    # removed-fix / re-added-bug: only warn for commits classified at or above this severity
    min_severity: int = 2
    # forgot-related-file: confidence that B changes when A changes, and minimum joint commits
    cochange_min_confidence: float = 0.8
    cochange_min_support: int = 5
    # skip commits touching more files than this when mining co-change (mass reformat, renames)
    cochange_max_files_per_commit: int = 30
    disabled_checks: list[str] = field(default_factory=list)
    ignore_paths: list[str] = field(default_factory=list)


def load_config(repo: str) -> Config:
    # TODO(M1): parse pyproject.toml / .blot.toml with tomllib (3.11+), defaults on 3.10
    return Config()
