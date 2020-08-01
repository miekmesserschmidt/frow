import fitz
import os
import pytest
from frow.tools import file_transform, inspect

def test_ensure_path(tmp_path):
    p = os.path.join(tmp_path, "a")
    file_transform.ensure_path(p)

    assert os.path.isdir(p)


def test_copy_file(tmp_path):
    a = os.path.join(tmp_path, "a")
    b = os.path.join(tmp_path, "b")

    with open(a,"w") as f:
        f.write("a")
        
    with open(b,"w") as f:
        f.write("b")

    file_transform.copy_file(a,b, overwrite=True)

    with open(b,"r") as f:
        assert f.read() == "a"


def test_copy_file_no_overwrite(tmp_path):
    a = os.path.join(tmp_path, "a")
    b = os.path.join(tmp_path, "b")

    with open(a,"w") as f:
        f.write("a")
        
    with open(b,"w") as f:
        f.write("b")

    file_transform.copy_file(a,b, overwrite=False)

    with open(b,"r") as f:
        assert f.read() == "b"


def test_ensure_pdf(tmp_path):
    source = "test/fixtures/img/00.jpg"
    dest = os.path.join(tmp_path, "a")

    file_transform.ensure_pdf(source,dest)
    assert inspect.is_pdf(dest)

    


def test_merge_pdf(tmp_path):

    L = [
        os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf"),
        os.path.join("test/fixtures/sub_folder_merge", "a", "1.pdf")
    ]
    out = os.path.join(tmp_path, "a.pdf")
    file_transform.merge_pdf(L, out)
    
    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 5 


def test_refit(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")


    file_transform.refit_pdf(fn, out, rect=.8* file_transform.A4)
    
    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 4
