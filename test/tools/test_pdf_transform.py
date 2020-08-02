import subprocess
import fitz
import os
import pytest
from frow.tools import pdf_transform, inspect


def test_refit(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")


    pdf_transform.refit_pdf(fn, out, relative_paste_rect=(0,0,.8,.8))
    
    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 4


def test_pdf_paste_on(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")

    doc = fitz.open(fn)
    source_doc = fitz.open(fn)

    pdf_transform.paste_pdf_on(doc[0], source_doc, (.5,.5,1,1))

    doc.save(out)

    # subprocess.call(["xdg-open", out])

