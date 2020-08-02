
import numpy as np
import os
import shutil
import fitz
from . import inspect, decorators, file_transform, box
 


A4 = np.array((0, 0, 595, 842))

@decorators.with_overwrite_toggle
def refit_pdf(source_fn, dest_fn, relative_paste_rect=None, abs_paste_rect=None, border=True): #TODO relative rect
    assert not (relative_paste_rect and abs_paste_rect)  

    if not relative_paste_rect and not abs_paste_rect:
        abs_paste_rect = A4
    elif relative_paste_rect:
        abs_paste_rect = box.absolute_box(relative_paste_rect, A4)


    source_pdf = fitz.open(source_fn)

    d = fitz.open()

    for i, page in enumerate(source_pdf.pages()):

        new_page = d.newPage()
        new_page.showPDFpage(
            abs_paste_rect, source_pdf, pno=i,
        )

        if border:
            new_page.drawRect(abs_paste_rect, overlay=True)

    path, _ = os.path.split(dest_fn)
    file_transform.ensure_path(path)

    d.save(dest_fn)
    return dest_fn


def paste_pdf_on(fitzpage, source, relative_rect, **kwargs):
    abs_rect = box.absolute_box(relative_rect, fitzpage.rect)
    fitzpage.showPDFpage(abs_rect, source, **kwargs)
    return fitzpage

    

