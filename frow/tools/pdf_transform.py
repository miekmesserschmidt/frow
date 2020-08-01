import numpy as np
import os
import shutil
import fitz
from . import inspect, decorators, file_transform
 


A4 = np.array((0, 0, 595, 842))

@decorators.with_overwrite_toggle
def refit_pdf(source_fn, dest_fn, rect=A4, border=True):
    source_pdf = fitz.open(source_fn)

    R = fitz.Rect(*rect)
    d = fitz.open()

    for i, page in enumerate(source_pdf.pages()):
        new_page = d.newPage()
        new_page.showPDFpage(
            R, source_pdf, pno=i,
        )

        if border:
            new_page.drawRect(R, overlay=True)

    path, _ = os.path.split(dest_fn)
    file_transform.ensure_path(path)

    d.save(dest_fn)
    return dest_fn
