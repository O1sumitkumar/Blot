import pytest

from blot.classify import CommitInfo, fix_severity, is_refactor, linked_issues


def commit(subject, body="", files=1, added=5, removed=5, renames=0):
    return CommitInfo("abc", subject, body, files, added, removed, renames)


@pytest.mark.parametrize(
    "subject, body, expected",
    [
        ("Break reference cycle created by default in Flask instances.", "", 2),  # the Flask case
        ("Fix crash when session is empty", "", 2),
        ("Handle empty session", "Fixes #3761", 2),
        ("Fix typo in docs", "Fixes #12", 1),  # issue-linked but routine
        ("fix lint", "", 1),
        ("Fix stuff", "", 1),
        ("Add dark mode", "Closes #44", 0),  # "closes" is housekeeping, not a fix
        ("Bump version to 2.1", "", 0),
        ("Prevent SQL injection in search", "", 2),
        ("Fix wrong status code on redirect", "", 2),  # weak defect word + fix verb
        ("Wrong status code on redirect", "", 0),  # weak defect word alone
        # real Flask subjects that must NOT be load-bearing
        ("Documented redirect behaviour. Fixes #42", "", 1),
        ("Fix incorrect references to query in testing doc", "", 1),
        ("Added a new example for checksums on input data.  This fixes #601", "", 1),
        ("Fix minor typo in security doc", "", 1),
        ("Added note on send_file security.", "", 0),
        ("fixed possible security problem in module branch", "", 2),
        ("Fix broken link to Flask-WTF", "", 1),
    ],
)
def test_fix_severity(subject, body, expected):
    assert fix_severity(commit(subject, body)) == expected


def test_bug_label_is_always_load_bearing():
    assert fix_severity(commit("Tweak parser"), issue_labels=["Bug"]) == 2


@pytest.mark.parametrize(
    "info, expected",
    [
        (commit("Split the App and Blueprint into Sansio and IO parts"), True),  # the Flask trap
        (commit("Reformat with black", files=40, added=900, removed=900), True),
        (commit("Update paths", files=4, renames=3), True),
        (commit("Fix crash after moving config loader"), False),  # fixes are never refactors
        (commit("Add retry logic", added=80, removed=2), False),
    ],
)
def test_is_refactor(info, expected):
    assert is_refactor(info) is expected


def test_linked_issues_dedupes_in_order():
    info = commit("Fix race in pool (#12)", "Fixes #12, see also gh-7 and JIRA-42. Not a URL: http://x/#3")
    assert linked_issues(info) == ["#12", "gh-7", "JIRA-42"]
