from blot.config import Config, load_config


def test_defaults_without_files(tmp_path):
    assert load_config(str(tmp_path)) == Config()


def test_pyproject_then_own_file_wins(tmp_path, capsys):
    (tmp_path / "pyproject.toml").write_text(
        '[tool.blot]\nmin-severity = 1\ncochange-min-confidence = 1\ndisabled-checks = ["readded-bug"]\n',
        encoding="utf-8",
    )
    (tmp_path / ".blot.toml").write_text("min_severity = 2\nbogus = 3\ncochange_min_support = 'many'\n", encoding="utf-8")
    config = load_config(str(tmp_path))
    assert config.min_severity == 2
    assert config.cochange_min_confidence == 1.0
    assert config.disabled_checks == ["readded-bug"]
    assert config.cochange_min_support == 5
    err = capsys.readouterr().err
    assert "unknown config key 'bogus'" in err and "'cochange_min_support' should be int" in err


def test_broken_toml_falls_back_to_defaults(tmp_path, capsys):
    (tmp_path / ".blot.toml").write_text("min_severity = = 2\n", encoding="utf-8")
    assert load_config(str(tmp_path)) == Config()
    assert "ignoring .blot.toml" in capsys.readouterr().err
