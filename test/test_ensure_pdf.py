import pytest
import subprocess
import os 
from frow import ensure_pdf, inspect


img_path = "test/fixtures/img"


@pytest.mark.parametrize("img_fn", [
    ("01.jpg"),
    ("00.jpg.pdf"),
    ("04.png"),
])
def test_ensure_pdf_one(tmp_path, img_fn):
    fn = os.path.join(img_path, img_fn)
    out_fn = os.path.join(tmp_path,"out.pdf")
    ensure_pdf.one(fn,  dest =out_fn)

    assert inspect.is_pdf(out_fn)

    with pytest.raises(FileExistsError):
        ensure_pdf.one(fn,  dest =out_fn, override=False)


def test_ensure_pdf_bulk():
    tmp_path = "tmp"
    source = img_path    
    dest = os.path.join(tmp_path, "out")

    ensure_pdf.bulk(source, dest)

    assert inspect.is_pdf(dest)


def test_ensure_pdf_bulk_no_override():
    tmp_path = "tmp"
    source = img_path    
    dest = os.path.join(tmp_path, "out")

    ensure_pdf.bulk(source, dest)

    with pytest.raises(FileExistsError):
        ensure_pdf.bulk(source, dest, silent_errors=False, override=False)
