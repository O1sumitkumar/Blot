"""Check registry."""

from __future__ import annotations

from blot.checks.base import Check, Finding
from blot.checks.cochange import ForgotRelatedFile
from blot.checks.readded_bug import ReaddedBug
from blot.checks.removed_fix import RemovedFix
from blot.config import Config

REGISTRY: list[type[Check]] = [RemovedFix, ReaddedBug, ForgotRelatedFile]


def all_checks(config: Config) -> list[Check]:
    return [cls() for cls in REGISTRY if cls.id not in config.disabled_checks]


__all__ = ["REGISTRY", "Check", "Finding", "all_checks"]
