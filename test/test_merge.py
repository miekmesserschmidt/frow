import fitz
import pytest
import subprocess
import os 
from frow import ensure_pdf, inspect, merge


sub_folder_merge_path = "test/fixtures/sub_folder_merge"


def test_merge(tmp_path):

    L = [
        os.path.join(sub_folder_merge_path, "a", "0.pdf"),
        os.path.join(sub_folder_merge_path, "a", "1.pdf")
    ]
    out = os.path.join(tmp_path, "a.pdf")
    merge.merge(L, out)
    
    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 5


def test_merge_no_override(tmp_path):

    L = [
        os.path.join(sub_folder_merge_path, "a", "0.pdf"),
        os.path.join(sub_folder_merge_path, "a", "1.pdf")
    ]
    out = os.path.join(tmp_path, "a.pdf")
    merge.merge(L, out)
    
    with pytest.raises(FileExistsError):
        merge.merge(L, out, override=False)


def test_subfolder_merge(tmp_path):

    merge.subfolder_merge(sub_folder_merge_path, tmp_path)

    a = os.path.join(tmp_path,"a.pdf")
    b = os.path.join(tmp_path,"b.pdf")
    assert inspect.is_pdf(a)
    assert inspect.is_pdf(b)

    A = fitz.open(a)
    B = fitz.open(b)
    assert A.pageCount == 5
    assert B.pageCount == 3

    
def test_subfolder_merge_no_override(tmp_path):

    merge.subfolder_merge(sub_folder_merge_path, tmp_path)

    with pytest.raises(FileExistsError):
        merge.subfolder_merge(sub_folder_merge_path, tmp_path, override=False)


    
