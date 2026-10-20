from blot.diff import parse_unified_diff, read_changes

SAMPLE = """\
diff --git a/app.py b/app.py
index 1111111..2222222 100644
--- a/app.py
+++ b/app.py
@@ -10,2 +10 @@ def setup():
-    self_ref = weakref.ref(self)
-    view = lambda: self_ref().send()
+    view = lambda: self.send()
diff --git a/new.py b/new.py
new file mode 100644
--- /dev/null
+++ b/new.py
@@ -0,0 +1,2 @@
+x = 1
+y = 2
"""


def test_parse_removed_and_added_lines():
    app, new = parse_unified_diff(SAMPLE)
    assert app.path == "app.py" and app.old_path == "app.py"
    assert app.removed == [(10, "    self_ref = weakref.ref(self)"), (11, "    view = lambda: self_ref().send()")]
    assert app.added == [(10, "    view = lambda: self.send()")]
    assert new.old_path is None
    assert new.added == [(1, "x = 1"), (2, "y = 2")]


def test_read_staged_changes(make_repo):
    repo = make_repo([("feat: add a", {"a.py": "one\ntwo\n"})])
    (repo / "a.py").write_text("one\nTWO\n", encoding="utf-8")
    import subprocess

    subprocess.run(["git", "-C", str(repo), "add", "a.py"], check=True)
    (change,) = read_changes(str(repo))
    assert change.removed == [(2, "two")]
    assert change.added == [(2, "TWO")]
