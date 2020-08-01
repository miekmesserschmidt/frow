import os
import pytest

import frow.structure as structure


fixture_path = "test/fixtures/structure"



def test_cp_structure_func(tmp_path):

    fn = "crap_u43214322__asdf.txt"
    source_path = os.path.join(fixture_path, "st_num",fn)

    structure.cp_structure_func(source_path,  tmp_path)

    out_fn = os.path.join(tmp_path, fn)
    assert os.path.isfile(out_fn)


    with pytest.raises(FileExistsError):
        structure.cp_structure_func(source_path,  tmp_path, override=False)



def test_st_num_structure_func(tmp_path):

    fn = "crap_u43214322__asdf.txt"
    source_path = os.path.join(fixture_path, "st_num", fn)

    structure.st_num_structure_func(source_path, tmp_path)

    out_fn = os.path.join(tmp_path, "u43214322", fn)
    assert os.path.isfile(out_fn)

    with pytest.raises(FileExistsError):
        structure.st_num_structure_func(source_path, tmp_path, override=False)


def test_bulk(tmp_path):

    fns = [
        "crap_u43214322__asdf.txt",
        "starting_u43214321__asdf.txt",
    ]

    source_path = os.path.join(fixture_path, "st_num")
    structure.bulk(source_path, tmp_path, structure_func=structure.st_num_structure_func, silent_errors=False)

    out_fn = os.path.join(tmp_path, "u43214322", fns[0])
    assert os.path.isfile(out_fn)

    out_fn = os.path.join(tmp_path, "u43214321", fns[1])
    assert os.path.isfile(out_fn)


def test_bulk_no_override(tmp_path):


    source_path = os.path.join(fixture_path, "st_num")
    structure.bulk(source_path, tmp_path, structure_func=structure.st_num_structure_func, silent_errors=False)

    with pytest.raises(FileExistsError):
        structure.bulk(source_path, tmp_path, structure_func=structure.st_num_structure_func, silent_errors=False, override=False)


def test_bulk_errors(tmp_path):

    source_path = os.path.join(fixture_path, "st_num_fail")

    with pytest.raises(NameError):
        structure.bulk(source_path, tmp_path, structure_func=structure.st_num_structure_func, silent_errors=False)

