import fitz
import os
import pytest
from frow.tools import pdf_transform, inspect


def test_refit(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")


    pdf_transform.refit_pdf(fn, out, rect=.8* pdf_transform.A4)
    
    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 4
