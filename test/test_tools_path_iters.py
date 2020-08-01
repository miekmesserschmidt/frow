import os, pytest
import frow.tools.path_iters as tools


fixture_path = "test/fixtures/walk"

@pytest.mark.parametrize("iter_type, expected", [
    (tools.FilesRecursive, set(["a","d/b","b/a"])),
    (tools.DirsRecursive, set(["b", "d", "b/c"])),
    (tools.FilesNonRecursive, set(["a"])),
    (tools.DirsNonRecursive, set(["b", "d"])),
])
def test_files_iter(iter_type, expected):
    out = set(d for _, d in iter_type(fixture_path))

    assert set(out) == expected


@pytest.mark.parametrize("iter_type, expected", [
    (tools.FilesRecursive, set(["a","d/b","b/a"])),
    (tools.DirsRecursive, set(["b", "d", "b/c"])),
    (tools.FilesNonRecursive, set(["a"])),
    (tools.DirsNonRecursive, set(["b", "d"])),
])
def test_files_iter_joined(iter_type, expected):
    out = set(d for d in iter_type(fixture_path).joined())

    assert set(out) == set( os.path.join(fixture_path,f) for f in expected)


