"""
Tools for manipulating fitz pdf pages and documents
"""

from PIL import Image
import io
import numpy as np
import os
import shutil
import fitz
from . import inspect
from ..other import box


A4 = np.array((0, 0, 595, 842))


def refit_pdf(
    in_, relative_paste_rect=None, abs_paste_rect=None, border=True,
):
    """Refits all pages of a pdf. Used, e.g., to shrink pages' content a bit. 

    Args:
        in_ ([fitz doc]): Document to refit
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        border : add a border. Defaults to True.

    Returns:
        [fitz doc]: Refitted fitz doc
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


def merge_pdf(source_list,):
    """Merges all fitz docs in source_list into one pdf fitz doc in the order provided.
    
    Args:
        source_list ([list of fitz docs]): List of fitz documents to merge

    Returns:
        [fitz doc]: merged fitz doc
    """
    b = fitz.open()
    for a in source_list:
        b.insertPDF(a)

    return b


def open_ensuring_pdf(source_fn, constructor = fitz.open):
    """Opens a file ensuring that it is a pdf. Images are converted to pdf.
    
    Use the constructor parameter to allow different instantiations (e.g., multiprocessing friendly wrapper for fitz docs)

    Args:
        source_fn ([str]): source filename
        constructor ([type], optional):  Defaults to fitz.open.

    Returns:
        [fitz doc]: Opened fitz document
    """
    if inspect.is_pdf(source_fn):
        return constructor(source_fn)
    else:
        s = constructor(source_fn)
        d = constructor(stream=s.convertToPDF(), filetype="pdf")
        return d


def paste_pdf_on(fitz_page, source_doc, relative_rect=None, absolute_rect=None, **kwargs):

    """Pastes a source document onto the given fitz page.


    Args:
        fitz_page : page to paste onto
        source_doc : document to paste from
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        kwargs : passed to fitz_page.showPDFpage (look up fitz options, e.g. different page)

    Returns:
        fitz_page
    """
    abs_paste_rect = box.ensure_absolute_box(
        relative_rect, absolute_rect, fitz_page.rect
    )

    fitz_page.showPDFpage(abs_paste_rect, source_doc, **kwargs)
    return fitz_page


def paste_pdf_on_every_page(
    fitz_doc, source_doc, relative_rect=None, absolute_rect=None, **kwargs
):
    """Pastes a source document onto the given fitz page.


    Args:
        fitz_doc : doc to paste on
        source_doc : document to paste from
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        kwargs : passed to fitz_page.showPDFpage (look up options)

    Returns:
        fitz_page
    """
    for p in fitz_doc.pages():
        paste_pdf_on(
            p,
            source_doc,
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
    fitz_page, relative_rect=None, absolute_rect=None, zoom=1,
):
    """Crops the given rect of a page to a pillow.Image. 

    Args:
        fitz_page ([fitz page]): pdf page to crop
        relative_rect : relative rect to paste into (one of relative_rect and absolute_rect must be None)
        absolute_rect : absolute rect to paste into (one of relative_rect and absolute_rect must be None)
        zoom (int, optional): zoom level. Defaults to 1.

    Returns:
        [PIL.Image]: Image of the crop
    """
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


def doc_from_pages(fitz_pages,):
    """Given a list of fitz pages, create a fitz doc with those pages

    Args:
        fitz_pages ([list of fitz pages]): Fits pages to make a new doc from

    Returns:
        [fitz doc]: A new fitz doc, with the provided pages
    """
    doc = fitz.open()
    for p in fitz_pages:
        *_, w, h = p.rect
        new_page = doc.newPage(width=w, height=h)
        paste_pdf_on(new_page, p.parent, absolute_rect=p.rect, pno=p.number)

    return doc

