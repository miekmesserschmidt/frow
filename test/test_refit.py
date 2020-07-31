import fitz
import pytest
import subprocess
import os 
from frow import ensure_pdf, inspect, merge, refit




sub_folder_merge_path = "test/fixtures/sub_folder_merge"


def test_refit(tmp_path):

    fn = os.path.join(sub_folder_merge_path, "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")


    refit.refit(fn, out, rect=.8*refit.A4)
    
    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 4
