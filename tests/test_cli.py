import pytest

from blot.checks import REGISTRY
from blot.cli import main
from blot.report import render
from blot.checks.base import Finding


def test_registry_has_three_checks():
    assert [c.id for c in REGISTRY] == ["removed-fix", "readded-bug", "forgot-related-file"]


def test_check_without_index_never_blocks(make_repo, capsys):
    repo = make_repo([("feat: init", {"a.py": "x = 1\n"})])
    assert main(["--repo", str(repo), "check"]) == 0
    assert "run `blot index`" in capsys.readouterr().err


def test_render_text():
    out = render([Finding("removed-fix", "app.py", 355, "You're changing a line added by a bug fix.", ['8efea0cc "Break reference cycle"'])])
    assert "1 warning" in out and "app.py:355" in out and "8efea0cc" in out


@pytest.mark.skip(reason="TODO(M2): needs index + checks implemented")
def test_removed_fix_traces_past_refactor(make_repo):
    """The Flask case in miniature: fix commit -> file split commit -> edit removes the fix."""
