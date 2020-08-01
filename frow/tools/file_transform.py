import numpy as np
import os
import shutil
import fitz
from . import inspect


def with_overwrite_toggle(f):
    def wrapper(source_fn, dest_fn, *args, overwrite=True, **kwargs):
        if os.path.isfile(dest_fn) and not overwrite:
            return dest_fn
        else:
            return f(source_fn, dest_fn, *args, **kwargs)

    return wrapper


def ensure_path(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


@with_overwrite_toggle
def copy_file(source_fn, dest_fn):
    path, _ = os.path.split(dest_fn)
    ensure_path(path)
    shutil.copyfile(source_fn, dest_fn)

    return dest_fn


@with_overwrite_toggle
def ensure_pdf(source_fn, dest_fn):
    if inspect.is_pdf(source_fn):
        return copy_file(source_fn, dest_fn, overwrite=overwrite)
    else:
        s = fitz.open(source_fn)

        path, _ = os.path.split(dest_fn)
        ensure_path(path)

        with open(dest_fn, "wb") as f:
            f.write(s.convertToPDF())

        return dest_fn


@with_overwrite_toggle
def merge_pdf(source_list, dest_fn, override=True):
    b = fitz.open()
    for source_fn in source_list:
        a = fitz.open(source_fn)
        b.insertPDF(a)

    path, _ = os.path.split(dest_fn)
    ensure_path(path)

    b.save(dest_fn)
    return dest_fn


A4 = np.array((0, 0, 595, 842))


@with_overwrite_toggle
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
    ensure_path(path)

    d.save(dest_fn)
    return dest_fn
