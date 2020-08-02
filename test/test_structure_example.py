import functional
import os
import pytest


from frow.tools import path_iters, file_transform
import frow.up


fixture_path = "test/fixtures/structure/st_num"


def test_structure(tmp_path):

    fns = [
        "crap_u43214322__asdf.txt",
        "starting_u43214321__asdf.txt",
    ]

    def make_source_dest_pair(source_fn, dest_path):
        st_num = frow.up.extract_first_st_num(source_fn)
        _, fn = os.path.split(source_fn)
        return source_fn, os.path.join(dest_path, st_num, fn)

    raw_fns = path_iters.FilesRecursive(fixture_path).joined()
    r = (
        functional.seq(raw_fns)  # ->(source_fn)
        .map_with_args_kwargs(
            make_source_dest_pair, dest_path=tmp_path
        )  # ->(source_fn, dest_fn)
        .starmap_with_args_kwargs(
            file_transform.copy_file, overwrite=True
        )  # ->(dest_fn)
    ).list()

    print(r)

    out_fn = os.path.join(tmp_path, "u43214322", fns[0])
    assert os.path.isfile(out_fn)

    out_fn = os.path.join(tmp_path, "u43214321", fns[1])
    assert os.path.isfile(out_fn)

