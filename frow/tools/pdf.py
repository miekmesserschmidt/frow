from PIL import Image
import io
import numpy as np
import os
import shutil
import fitz
from . import inspect, box


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



def open_ensuring_pdf(source_fn):
    if inspect.is_pdf(source_fn):
        return fitz.open(source_fn)
    else:
        s = fitz.open(source_fn)
        d = fitz.open(stream=s.convertToPDF(), filetype="pdf")
        return d


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
    abs_paste_rect = box.ensure_absolute_box(
        relative_rect, absolute_rect, fitz_page.rect
    )

    fitz_page.showPDFpage(abs_paste_rect, source, **kwargs)
    return fitz_page



def paste_pdf_on_every_page(
    fitz_doc, source, relative_rect=None, absolute_rect=None, **kwargs
):

    """Pastes a source document onto the given fitz page.


    Args:
        fitz_doc : doc to paste on
        source : document to paste from
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        kwargs : passed to fitz_page.showPDFpage (look up options)

    Returns:
        fitz_page
    """
    for p in fitz_doc.pages():
        paste_pdf_on(
            p,
            source,
            relative_rect=relative_rect,
            absolute_rect=absolute_rect,
            **kwargs
        )

    return fitz_doc


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


def crop_to_pillow_image(
    fitz_page,
    relative_rect=None,
    absolute_rect=None,
    zoom=1,
):
    absolute_rect = box.ensure_absolute_box(
        relative_rect, absolute_rect, fitz_page.rect
    )

    matrix = fitz.Matrix(zoom, zoom)
    orig_crop_box = fitz_page.CropBox
    
    fitz_page.setCropBox(absolute_rect)
    data = fitz_page.getPixmap(matrix=matrix).getImageData()
    fitz_page.setCropBox(orig_crop_box)

    im = Image.open(io.BytesIO(data))
    return im


def doc_from_pages(fitz_pages):
    doc = fitz.open()
    for p in fitz_pages:
        *_, w,h =p.rect
        new_page = doc.newPage(width = w, height = h)
        paste_pdf_on(
            new_page,
            p.parent,
            absolute_rect=p.rect,
            pno = p.number
        )

    return doc
    