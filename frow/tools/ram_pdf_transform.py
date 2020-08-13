import numpy as np
import os
import shutil
import fitz
from . import inspect, decorators, file_transform, box


A4 = np.array((0, 0, 595, 842))


def refit_pdf(
    in_,
    relative_paste_rect=None,
    abs_paste_rect=None,
    border=True,
):
    """Refits all pages of a pdf. Used, e.g., to shrink pages' content a bit.

    Args:
        source_fn : Source pdf filename
        dest_fn : Destination pdf filename
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        border : add a border. Defaults to True.

    Returns:
        fitz_doc
    """
    abs_paste_rect = box.ensure_absolute_box(relative_paste_rect, abs_paste_rect, A4)

    source_pdf = in_

    d = fitz.open()

    for i, page in enumerate(source_pdf.pages()):

        new_page = d.newPage()
        new_page.showPDFpage(
            abs_paste_rect, source_pdf, pno=i,
        )

        if border:
            new_page.drawRect(abs_paste_rect, overlay=True)

    return d 



def merge_pdf(source_list, ):
    b = fitz.open()
    for a in source_list:        
        b.insertPDF(a)

    return b
