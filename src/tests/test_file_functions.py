import os
import pytest
from file_functions import check_dir, copy_dir_content


class TestCheckDir:
    def test_nonexistent_dir_raises(self, tmp_path):
        nonexistent = str(tmp_path / "does_not_exist")
        with pytest.raises(Exception, match="not found"):
            check_dir(nonexistent)

    def test_file_path_raises(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("hello")
        with pytest.raises(Exception, match="is a file"):
            check_dir(str(f))

    def test_valid_directory_does_not_raise(self, tmp_path):
        check_dir(str(tmp_path))  # Should not raise


class TestCopyDirContent:
    def test_same_source_and_target_raises(self, tmp_path):
        path = str(tmp_path / "dir")
        with pytest.raises(Exception, match="into itself"):
            copy_dir_content(path, path)

    def test_copies_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        src = tmp_path / "src"
        src.mkdir()
        (src / "file.txt").write_text("hello")

        copy_dir_content("src", "dst")

        dst = tmp_path / "dst"
        assert dst.is_dir()
        assert (dst / "file.txt").read_text() == "hello"

    def test_copies_nested_directories(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        src = tmp_path / "src"
        sub = src / "sub"
        sub.mkdir(parents=True)
        (sub / "nested.txt").write_text("nested content")

        copy_dir_content("src", "dst")

        assert (tmp_path / "dst" / "sub" / "nested.txt").read_text() == "nested content"

    def test_replaces_existing_target(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        src = tmp_path / "src"
        src.mkdir()
        (src / "new.txt").write_text("new")

        dst = tmp_path / "dst"
        dst.mkdir()
        (dst / "old.txt").write_text("old")

        copy_dir_content("src", "dst")

        assert (tmp_path / "dst" / "new.txt").exists()
        assert not (tmp_path / "dst" / "old.txt").exists()

    def test_nonexistent_source_logs_error_and_returns(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        # Should not raise, just log an error and return
        copy_dir_content("nonexistent_src", "dst")
        assert not (tmp_path / "dst").exists()

    def test_copies_multiple_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        src = tmp_path / "src"
        src.mkdir()
        (src / "a.txt").write_text("a")
        (src / "b.txt").write_text("b")
        (src / "c.txt").write_text("c")

        copy_dir_content("src", "dst")

        dst = tmp_path / "dst"
        assert (dst / "a.txt").read_text() == "a"
        assert (dst / "b.txt").read_text() == "b"
        assert (dst / "c.txt").read_text() == "c"
