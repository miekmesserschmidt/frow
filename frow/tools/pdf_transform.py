import numpy as np
import os
import shutil
import fitz
from . import inspect, decorators, file_transform, box


A4 = np.array((0, 0, 595, 842))


@decorators.with_overwrite_toggle
def refit_pdf(
    source_fn, dest_fn, relative_paste_rect=None, abs_paste_rect=None, border=True
):
    """Refits all pages of a pdf. Used, e.g., to shrink pages' content a bit.

    Args:
        source_fn : Source pdf filename
        dest_fn : Destination pdf filename
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        border : add a border. Defaults to True.

    Returns:
        dest_fn
    """
    assert not (relative_paste_rect is not None and abs_paste_rect is not None)

    if not relative_paste_rect is not None and not abs_paste_rect is not None:
        abs_paste_rect = A4
    elif relative_paste_rect is not None:
        abs_paste_rect = box.absolute_box(relative_paste_rect, A4)

    source_pdf = fitz.open(source_fn)

    d = fitz.open()

    for i, page in enumerate(source_pdf.pages()):
        # page_abs_paste_rect = fitz.Rect(abs_paste_rect).transform(page.rotationMatrix)

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


def paste_pdf_on(fitz_page, source, relative_rect=None, absolute_rect=None, **kwargs):

    """Pastes a source document onto the given fitz page.


    Args:
        fitz_page : page to paste onto
        source : document to paste from
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        kwargs : passed to fitz_page.showPDFpage (look up options)

    Returns:
        fitz_page
    """
    assert not (relative_rect is not None and absolute_rect is not None)

    if not relative_rect is not None and not absolute_rect is not None:
        absolute_rect = A4
    elif relative_rect is not None:
        abs_paste_rect = box.absolute_box(relative_rect, fitz_page.rect)

    abs_rect = fitz.Rect(box.absolute_box(relative_rect, fitz_page.rect)).transform(
        fitz_page.rotationMatrix
    )
    fitz_page.showPDFpage(abs_rect, source, **kwargs)
    return fitz_page


# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF
import io


def svg_plonk(fitz_doc):
    """
    Copies a fitz document through converting each page to svg first. 
    
    This is done so that e.g., rotations of pages are fixed to 0.

    Args:
        fitz_doc : a fitz document

    Returns:
        fitz_doc : a new fitz document
    """
    d = fitz.open()

    for page in fitz_doc.pages():
        _, _, w, h = in_rect = page.rect
        svg_data = page.getSVGimage()

        pdf_data = fitz.open("svg", stream=io.BytesIO(svg_data.encode())).convertToPDF()
        src = fitz.open("pdf", stream=io.BytesIO(pdf_data))

        p = d.newPage(width=w, height=h)
        p.showPDFpage(in_rect, src)

    return d

