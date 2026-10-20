"""Check 1: you're deleting or editing lines that a load-bearing bug fix added.

Algorithm:
    1. for each file, take the removed lines (old line numbers)
    2. `git blame -w -M -C --porcelain -L a,b HEAD -- <old_path>` for those ranges
    3. if the blamed commit is a refactor (classify.is_refactor), re-blame at its parent
       on the original path, up to 3 hops
    4. warn if the final commit's severity >= config.min_severity
"""

from __future__ import annotations

from blot.checks.base import Check, Finding


class RemovedFix(Check):
    id = "removed-fix"
    description = "Changing code that a bug fix added"

    def run(self, changes, store, config) -> list[Finding]:
        # TODO(M2): implement the algorithm above. Batch blame per file to stay fast.
        return []
