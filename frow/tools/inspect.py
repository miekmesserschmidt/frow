import itertools
import os
import fitz
import shutil
import tqdm


def _is_pdf_single(fn):
    """True if the fn is a pdf, else False

    Args:
        fn (str): filename

    Returns:
        [bool]: True if fn is a pdf, else False
    """
    s = fitz.open(fn)
    return "PDF" in s.metadata["format"]


def _is_pdf_all(path):
    """True if all the files at the path (recursively traversed) are pdf, else False.


    Args:
        path ([str]): Path to test

    Returns:
        [bool]: 
    """
    for root, dirs, files in os.walk(path):
        for fn in files:
            p = os.path.join(root, fn)
            if not _is_pdf_single(p):
                return False

    else:
        return True


def is_pdf(path):
    """True if path is a pdf, or if all the files at the path (recursively traversed) are pdf, else False.

    Args:
        path ([str]): Path to test

    Returns:
        [bool]: 
    """    
    if os.path.isdir(path):
        return _is_pdf_all(path)
    else:
        return _is_pdf_single(path)
