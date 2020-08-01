import itertools
import os
import fitz
import shutil
import tqdm


        


def _is_pdf_single(fn):
    s = fitz.open(fn)
    return "PDF" in s.metadata["format"]

def _is_pdf_all(path):
    for root, dirs, files in os.walk(path):
        for fn in files:
            p = os.path.join(root, fn)
            if not _is_pdf_single(p):
                return False

    else:
        return True



def is_pdf(path):
    if os.path.isdir(path):
        return _is_pdf_all(path)
    else:
        return _is_pdf_single(path)