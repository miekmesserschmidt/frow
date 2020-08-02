import numpy as np
import os
import shutil
import fitz
from . import inspect, decorators




def ensure_path(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


@decorators.with_overwrite_toggle
def copy_file(source_fn, dest_fn, overwrite=True):
    path, _ = os.path.split(dest_fn)
    ensure_path(path)
    shutil.copyfile(source_fn, dest_fn)

    return dest_fn


@decorators.with_overwrite_toggle
def ensure_pdf(source_fn, dest_fn, overwrite=True):
    if inspect.is_pdf(source_fn):
        return copy_file(source_fn, dest_fn, overwrite=overwrite)
    else:
        s = fitz.open(source_fn)

        path, _ = os.path.split(dest_fn)
        ensure_path(path)

        with open(dest_fn, "wb") as f:
            f.write(s.convertToPDF())

        return dest_fn


@decorators.with_overwrite_toggle
def merge_pdf(source_list, dest_fn, overwrite=True):
    b = fitz.open()
    for source_fn in source_list:
        a = fitz.open(source_fn)
        b.insertPDF(a)

    path, _ = os.path.split(dest_fn)
    ensure_path(path)

    b.save(dest_fn)
    return dest_fn

