import itertools
import os
import fitz
import shutil
import tqdm
import pathlib

import logging

logger = logging.getLogger(__name__)

def merge(source_list, dest, override = True):

    if os.path.isfile(dest) and not override:
        raise FileExistsError(f"{dest} exists")

    b = fitz.open()

    for source_fn in source_list:
        a = fitz.open(source_fn)
        b.insertPDF(a)

    
    b.save(dest)
    



def subfolder_merge(source, dest, silent_errors=False, override=True):
    for root, dirs, files in os.walk(source):

        if not files:
            continue


        sources = sorted([os.path.join(root, fn) for fn in files])

        parent = os.path.split(root)[-1]
        dest_fn = os.path.join(dest, f"{parent}.pdf")

        try:
            merge(sources, dest_fn, override=override)
        except Exception as e:
            logger.exception(f"Failed merging {sources} into {dest_fn}", stack_info=True)
            if not silent_errors:
                raise e
            if silent_errors and isinstance(e, KeyboardInterrupt):
                raise e
