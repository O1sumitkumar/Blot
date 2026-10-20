"""Check 3: you changed A, but B almost always changes with A, and B isn't staged.

Algorithm (association rules over commit history):
    support(A, B)    = number of commits touching both A and B
    confidence(A→B)  = support(A, B) / commits touching A
    warn when confidence >= config.cochange_min_confidence
          and support    >= config.cochange_min_support
          and B exists at HEAD and is not part of the change
Commits touching more than config.cochange_max_files_per_commit files are ignored
(mass reformatting and renames would otherwise link everything to everything).
"""

from __future__ import annotations

from blot.checks.base import Check, Finding


class ForgotRelatedFile(Check):
    id = "forgot-related-file"
    description = "Changed a file without the file that usually changes with it"

    def run(self, changes, store, config) -> list[Finding]:
        # TODO(M2): implement the algorithm above; at most 1 finding per staged file
        return []
