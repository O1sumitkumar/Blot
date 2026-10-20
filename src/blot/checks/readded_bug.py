"""Check 2: you're adding back a line that a load-bearing bug fix deliberately removed.

Algorithm:
    1. normalize each added line (strip whitespace and trailing comments)
    2. skip trivial lines: shorter than 12 chars, only brackets/keywords, imports
    3. look up its hash in fix_removed_lines (same path, or any path if it was renamed)
    4. skip if an identical line still exists elsewhere in the file at HEAD
       (then the fix did not remove the idea, only one copy)
    5. warn with the fix commit that removed it
"""

from __future__ import annotations

from blot.checks.base import Check, Finding


class ReaddedBug(Check):
    id = "readded-bug"
    description = "Re-adding a line that a bug fix removed"

    def run(self, changes, store, config) -> list[Finding]:
        # TODO(M2): implement the algorithm above
        return []
