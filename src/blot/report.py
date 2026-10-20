"""Render findings for people (text) or tools (json)."""

from __future__ import annotations

import json
from dataclasses import asdict

from blot.checks.base import Finding


def render(findings: list[Finding], fmt: str = "text") -> str:
    if fmt == "json":
        return json.dumps([asdict(f) for f in findings], indent=2) + "\n"
    if not findings:
        return ""
    plural = "s" if len(findings) != 1 else ""
    lines = [f"blot: {len(findings)} warning{plural}", ""]
    for f in findings:
        where = f"{f.path}:{f.line}" if f.line else f.path
        lines.append(f"  ! {f.check}  {where}")
        lines.extend(f"    {text}" for text in f.message.splitlines())
        lines.extend(f"    {ref}" for ref in f.evidence)
        lines.append("")
    return "\n".join(lines) + "\n"
