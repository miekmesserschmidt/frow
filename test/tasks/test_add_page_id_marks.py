
import subprocess
import fitz
import os
import pytest
import frow.tasks.tasks as tasks


import pytest

def test_add_page_id_marks(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")

    doc = fitz.open(fn)

    tasks.add_page_id_marks(doc, relative_rect= (.8,.9,.95,.99), doc_id = "4444")


    doc.save(out)

    # subprocess.call(["xdg-open", out])

