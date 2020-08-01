import itertools
import os
import fitz
import shutil
import tqdm

import logging

logger = logging.getLogger(__name__)

from . import inspect
        

    
def ensure_folder(path):
    p, f = os.path.split(path)
    try:
        os.makedirs(p)
    except FileExistsError:
        pass


def one(source, dest, override=True):
    if os.path.isfile(dest) and not override:
        raise FileExistsError(f"dest exists {source} -> {dest}")

    if inspect.is_pdf(source):
        shutil.copy(source, dest)
    else:
        ensure_folder(dest)
        s = fitz.open(source)        

        with open(dest, "wb") as f:
            f.write(s.convertToPDF())




def source_dest_pairs(source_path, dest_path, ensure_dest_paths=True):
    for root, dirs, files in os.walk(source_path):

        for fn in files:
            source = os.path.join(root, fn)
            dest = os.path.join(dest_path,fn)
            yield source, dest

def bulk(source_path, dest_path, silent_errors=False, override=True):
    sd = list(source_dest_pairs(source_path, dest_path, ensure_dest_paths=True))

    for s,d in tqdm.tqdm(sd, desc="Converting to pdf"):
        dest = f"{d}.pdf"
        try:
            one(s,dest, override=override)
        except Exception as e:
            logger.exception(f"Cannot ensure pdf {s} -> {dest} ", stack_info=True)
            if not silent_errors:
                raise e
            
            if isinstance(e, KeyboardInterrupt):
                raise e

