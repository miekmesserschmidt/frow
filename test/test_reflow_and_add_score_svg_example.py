import io
import subprocess
import functional
import os
import pytest
import fitz

from frow.tools import functional as _
from frow.tools import path_iters, file_transform, pdf_transform
import frow.up


fixture_path = "test/fixtures/structure/st_num"


def test_reflow_add_score(tmp_path):

    pdf_fn = "test/fixtures/sub_folder_merge/a/0.pdf"
    score_fn = "templates/bubbles_score.pdf"

    out_fn = os.path.join(tmp_path, "a.pdf")
    out_fnb = os.path.join(tmp_path, "b.pdf")

    pdf_transform.refit_pdf(pdf_fn, out_fn, rect=0.88 * pdf_transform.A4)

    doc = fitz.open(out_fn)
    score_doc = fitz.open(score_fn)

    score_rel_rect = (0.89, 0.6, 0.98, 0.88)

    result = (
        functional.seq(doc.pages())
            .map_with_args_kwargs(  
                pdf_transform.paste_pdf_on, source=score_doc, relative_rect=score_rel_rect
            )
    ).list()

    doc.save(out_fnb)

    # subprocess.call(["xdg-open", out_fnb])
