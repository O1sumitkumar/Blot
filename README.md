# Blot

[![CI](https://github.com/Sym-jay/Blot/actions/workflows/ci.yml/badge.svg)](https://github.com/Sym-jay/Blot/actions/workflows/ci.yml)

<img src="assets/sora/orange/idle.svg" width="112" alt="Sora, the Blot slime">

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

> **Status:** pre-alpha skeleton. Nothing is implemented yet. See [docs/PRD.md](docs/PRD.md).

## Quickstart (planned)

```bash
pip install blot-git
blot index            # one-time, builds .git/blot.db
blot install-hook     # adds a git pre-commit hook
```

Or with the [pre-commit](https://pre-commit.com) framework, see `.pre-commit-hooks.yaml`.

## Docs

- [What is this? (simple explanation)](docs/EXPLAINER.md)
- [Product requirements](docs/PRD.md)
- [Competitor tests](docs/competitors.md)
- [Contributing](CONTRIBUTING.md)

## License

MIT

Sora's body shape is based on [Animated Pixel Slime](https://rvros.itch.io/pixel-art-animated-slime) by rvros (CC0), recolored and given new expressions. Regenerate the sprites with `python assets/sora/build_sprites.py`.
