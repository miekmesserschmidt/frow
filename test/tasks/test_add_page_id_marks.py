import subprocess
import fitz
import os
import pytest
import frow.tasks.tasks as tasks
from frow.tools import qr


import pytest


def test_add_page_id_marks(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")

    doc = fitz.open(fn)

    tasks.add_page_id_marks(doc, {"doc_id":"4444"}, relative_rect=(0.8, 0.9, 0.95, 0.99),)

    doc.save(out)
    
    a = qr.read_json_qr(doc[0], zoom=4)
    assert a["page_index"] == 0
    assert a["doc_id"] == "4444"

    a = qr.read_json_qr(doc[1], zoom=4)
    assert a["page_index"] == 1
    assert a["doc_id"] == "4444"

    # subprocess.call(["xdg-open", out])

