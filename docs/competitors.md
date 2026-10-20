# Competitor tests: "why is this code here?" tools

Tested 2026-10-19 on Windows 11, Python 3.12, Node 24, against a full clone of `pallets/flask` (commit `d086db85`, 2026-10-07).

**Test case:** `src/flask/app.py` lines 348–358, the `weakref.ref(self)` lambda for the static route.
- **Correct answer:** commit `8efea0cc` (2020-10-03), *"Break reference cycle created by default in Flask instances"* (issue #3761).
- **Trap:** `git blame` points to `0ec7f713` (2023-06-11), *"Split the App and Blueprint into Sansio and IO parts"*. That commit only moved the code; it doesn't explain why the code exists. A good tool has to see past refactor and move commits.

## Summary

| Tool | Tested how | Ran on Windows? | Found the real reason? | Edit-time guard | Notes |
|---|---|---|---|---|---|
| **git-fence** (mythren, MIT, 2026-07-19) | README + repo metadata only (found late) | Not on stock Windows (hooks call `python3`; WSL needed) | Not tested | **Yes** — PreToolUse hook, ~30 ms, warns only on "load-bearing" fixes | **Closest to our plan.** Local SQLite index in `.git/`, `gh` for PR/issue data, two-tier classifier, benchmarked on Express. 1 commit, 0 stars, no activity since July |
| **code-archaeologist** (harsh1t3, MIT, last commit 2026-08-31) | Installed + ran (CLI, no API key) | After a fix (needs `colorama`, not declared) | **No.** Cited five 2010 commits. Missed `8efea0cc` | No | CLI + MCP + VS Code; CitationGuard; 1.1 s end-to-end; pip install took 3.5 min (heavy deps: FastAPI, watsonx SDK, google-genai) |
| **lore** (tt-a1i, Apache-2.0) | Ran via `npx` (`scan`, `why`, `guard`) | Yes | **No.** Reported `0ec7f713` (the refactor) with "attribution: none" | **Yes** — but only for notes taken from AI-agent transcripts or added by hand | Scanned 5,600 commits in 5 s. Useless for human-written history |
| **Codebase Time Machine** (hackathon, 5 commits) | Public demo in browser | n/a (web) | Not tested — demo failed: *"Failed to create repository record"* | No | Landing page shows "trusted by" logos and sample answers that appear made up |
| **Entire blame** | Docs only (needs Entire account and setup) | — | — | No | Adds context only for commits made while Entire was enabled |
| Others found by name search | GitHub search only | — | — | — | `malinda1986/whyline` (MCP memory for AI sessions), `CryptoGazer/WhyLine` (IDE plugin → Jira ticket), `SAL-Sovereign-AI-Labs/whyline` (IBM Bob attribution) |

## What we learned

1. **The idea is validated and crowded.** At least 8 projects appeared between May and October 2026, mostly hackathon entries. Almost none have users (0–3 stars) or keep being maintained.
2. **The edit-time guard isn't new.** git-fence built exactly that in July 2026. lore has a guard too, but it uses agent transcripts.
3. **Every tool we ran got the Flask case wrong.** Both stopped at the commit `git blame` returned and couldn't trace through a file move or split to the commit that explains the code. That's a real, measurable gap.
4. **Windows support is weak.** code-archaeologist crashed on Windows until we added `colorama`, and git-fence needs WSL.
5. **Nobody shares a benchmark.** git-fence reports its own numbers on Express. No public, labeled dataset exists of "lines that exist for a reason, with the correct explaining commit", so no tool's accuracy can be compared.

## What this meant for Blot
On-demand "why" tools and agent edit-time guards are already covered. Nobody has an open-source **commit-time** check that uses history to catch mistakes. So Blot is a pre-commit hook for every engineer, not just AI-agent users. It has three checks:
- **Removed fix:** overlaps with git-fence, but runs at commit time and traces past refactor commits.
- **Re-added bug:** no tool found.
- **Forgot the file that usually changes too:** no tool found.

Commit-time search on 2026-10-19 found only single-purpose hooks: [cffr's CITATION check](https://docs.ropensci.org/cffr/reference/cff_git_hook.html) and [GCC's revert-reference check](https://patchwork.sourceware.org/project/gcc/patch/f046d7d4-7dd4-28f2-10b9-6d266e3c0896@codesourcery.com/). History-based test selection exists only as paid tools ([Gradle Develocity](https://gradle.com/develocity/product-tour/accelerate/predictive-test-selection)) and experiments ([predictive-testing](https://github.com/harshit-bstack/predictive-testing)).

## Worth borrowing
- From code-archaeologist: the evidence ledger, plus a check that drops claims citing SHAs or PRs not in the evidence.
- From git-fence: a fast local index in `.git/`, warnings only for "load-bearing" commits, never blocking edits, silent failure.
- From lore: a `brief` command for SessionStart hook injection.
