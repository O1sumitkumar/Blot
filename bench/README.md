# Bench

Real changes from public repos, each labeled with what Blot **should** say.
This is how we keep warnings accurate and rare.

Each case in `cases.json` has:

| Field | Meaning |
|---|---|
| `repo`, `at` | public repo URL and the commit to check out |
| `change` | the edit to simulate, in words (scripted edits come later) |
| `file`, `lines` | where the edit happens |
| `expect.check` | which check should fire |
| `expect.warn` | `true` if it should warn, `false` if it must stay quiet |
| `expect.commit` | the commit the warning must cite |

Add **quiet cases** (`"warn": false`) as often as warning cases. They protect against false alarms.

Target for v0.1: 30 cases across 5 repos (Flask, Django, Express, React, requests).
