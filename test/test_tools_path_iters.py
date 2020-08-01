import os, pytest
import frow.tools.path_iters as tools


fixture_path = "test/fixtures/walk"


def test_files_recursive():
    out = set(d for _, d in tools.FilesRecursive(fixture_path))

    assert set(out) == set(["a","d/b","b/a"])




def test_folders_recursive():
    out = set(d for _, d in tools.DirsRecursive(fixture_path))

    assert set(out) == set(["b","b/c","d"])


def test_files_nonrecursive():
    out = set(d for _, d in tools.FilesNonRecursive(fixture_path))

    assert set(out) == set(["a"])




def test_folders_nonrecursive():
    out = set(d for _, d in tools.DirsNonRecursive(fixture_path))

    assert set(out) == set(["b","d"])

