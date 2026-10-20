# Blot, explained simply

> "Don't take down a fence until you know why it was put up."
> (G.K. Chesterton's idea, often called *Chesterton's fence*)

## The problem

Git remembers **what** changed in your code, but it doesn't warn you about the **why**.

Every project has lines that look pointless but are there for a reason: a strange null check, an odd `sleep(0.1)`, or two files that always have to be updated together. The reasons are buried in old commits, pull requests and issues that nobody reads before changing the code.

So the same mistakes keep happening:

- Someone "cleans up" a weird line, and a bug fixed two years ago comes back.
- Someone restores old code that was deleted on purpose because it was unsafe.
- Someone updates `schema.py` but forgets `migrations/`, as people have done many times before. CI fails 20 minutes later, or production breaks.

## A small story

Priya sees this in `app.py`:

```python
self_ref = weakref.ref(self)   # why not just use self?
```

It looks over-complicated, so she simplifies it and commits. Code review misses it too.
Three weeks later the app is leaking memory in production.

The line came from a 2020 commit, *"Break reference cycle created by default in Flask instances"* (issue #3761).
The information was there all along. Nothing showed it to her when it mattered.

## What Blot does

blot is a **check that runs when you `git commit`**. It has read your project's history and tells you when your change matches a mistake that history has seen before:

```
$ git commit -m "simplify static route"
blot: 1 warning

  ! removed-fix  src/flask/app.py:355
    You're changing a line added by a bug fix:
    8efea0cc "Break reference cycle created by default in Flask instances" (2020-10-03, fixes #3761)
    Make sure the original bug can't come back.

(commit allowed — use `blot why src/flask/app.py:355` for details)
```

In its first version it catches three kinds of mistake:

| | Check | Plain meaning |
|---|---|---|
| 1 | **Removed fix** | "You're deleting or changing code that was added to fix a bug." |
| 2 | **Re-added bug** | "You're adding back a line that a bug fix deliberately removed." |
| 3 | **Forgot related file** | "These two files almost always change together. You only changed one." |

It **warns, it doesn't block** (unless you choose strict mode). It's quiet by default: a check that cries wolf gets uninstalled.

## How it works (4 steps)

```
 ┌───────────────┐   ┌──────────────────┐   ┌───────────────┐   ┌───────────────┐
 │ 1. Index      │ → │ 2. Read your     │ → │ 3. Compare    │ → │ 4. Warn       │
 │ git history   │   │ staged change    │   │ against the   │   │ with links to │
 │ once (local)  │   │ (git diff)       │   │ index         │   │ the evidence  │
 └───────────────┘   └──────────────────┘   └───────────────┘   └───────────────┘
   fix commits,        added / removed        fast lookups,       commit, PR,
   removed lines,      lines per file         no AI needed        issue links
   co-change pairs
```

- It runs **locally**: no account and no server, and your code stays on your machine.
- It **doesn't need AI** for the core checks, so it's fast (under half a second) and free.
- It can optionally pull PR and issue details from GitHub to explain a warning better. Later, it can use an AI model to summarize why the code exists.

## Who it's for

- **Engineers** working in codebases older than they are.
- **Maintainers** tired of reviewing PRs that undo old fixes.
- **Teams using AI coding agents**: an agent's commit goes through the same check.
- **New contributors**, who don't know the project's history yet.

## What it is not

- Not a linter: it doesn't care about style.
- Not a replacement for tests or CI. It catches *history-shaped* mistakes earlier and more cheaply.
- Not a chat-with-your-repo bot.
