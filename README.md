# Blot

[![CI](https://github.com/Sym-jay/Blot/actions/workflows/ci.yml/badge.svg)](https://github.com/Sym-jay/Blot/actions/workflows/ci.yml)

<img src="assets/sora/orange/walk.svg" width="480" alt="Sora, the Blot slime, sliding back and forth">

**A pre-commit check that has read your project's history.**

Meet **Sora**, the slime who remembers every fix.

> Don't take down a fence until you know why it was put up.

Blot warns you *before you commit* when your change:

- **removes a fix**: deletes or edits code that was added to fix a bug
- **re-adds a bug**: brings back a line that a bug fix deliberately removed
- **forgets a related file**: changes `A` but not `B`, when the two almost always change together

It runs locally, needs no account or AI, and stays quiet unless the history gives it a real reason to speak.

```
$ git commit -m "simplify static route"
blot: 1 warning
  ! removed-fix  src/flask/app.py:355
    You're changing a line added by a bug fix:
    8efea0cc "Break reference cycle created by default in Flask instances" (fixes #3761)
```

> **Status:** pre-alpha. Milestone M1 is done: `blot index` builds the history index (Flask's 3,800 commits in ~2 s) and `blot install-hook` wires up git. The three checks land in M2, so `blot check` doesn't warn yet. See the [roadmap in the PRD](docs/PRD.md#12-milestones-4-weeks-part-time).

## Meet Sora

<img src="assets/sora/orange/faces.svg" width="168" alt="Sora cycling through expressions" align="right">

Sora is Blot's slime. You'll see a different face depending on what Blot finds:

| | Face | When |
|---|---|---|
| <img src="assets/sora/orange/idle.svg" width="84"> | Idle | Checking your commit |
| <img src="assets/sora/orange/happy.svg" width="84"> | Happy | Nothing to worry about |
| <img src="assets/sora/orange/alert.svg" width="84"> | Alert | Found a fence: this line fixed a bug |
| <img src="assets/sora/orange/worried.svg" width="84"> | Worried | Risky change, take a look |
| <img src="assets/sora/orange/sleepy.svg" width="84"> | Sleepy | Indexing history |
| <img src="assets/sora/orange/sad.svg" width="84"> | Sad | A fix is being removed |

Sora comes in four warm palettes:

<img src="assets/sora/orange/walk.svg" width="240" alt="Orange Sora"> <img src="assets/sora/sage/walk.svg" width="240" alt="Sage Sora">
<img src="assets/sora/blue/walk.svg" width="240" alt="Blue Sora"> <img src="assets/sora/mustard/walk.svg" width="240" alt="Mustard Sora">

## Quickstart

Not on PyPI yet, so install from GitHub:

```bash
pip install git+https://github.com/Sym-jay/Blot
cd your-repo
blot index            # one-time, builds .git/blot.db (refreshes incrementally after that)
blot install-hook     # adds Blot to .git/hooks/pre-commit without touching existing hooks
```

Remove it any time with `blot install-hook --uninstall`. Settings go in `[tool.blot]` in `pyproject.toml` or a `.blot.toml` file (see `src/blot/config.py`).

Or with the [pre-commit](https://pre-commit.com) framework, see `.pre-commit-hooks.yaml`.

## Docs

- [What is this? (simple explanation)](docs/EXPLAINER.md)
- [Product requirements](docs/PRD.md)
- [Competitor tests](docs/competitors.md)
- [Contributing](CONTRIBUTING.md)

## License

MIT

Sora's body shape is based on [Animated Pixel Slime](https://rvros.itch.io/pixel-art-animated-slime) by rvros (CC0), recolored and given new expressions. Regenerate the sprites with `python assets/sora/build_sprites.py`.
