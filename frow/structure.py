import os
import shutil
import re
import logging



logger = logging.getLogger(__name__)

def dest_exists(source_fn, dest_root):
    _, fn = os.path.split(source_fn)        
    dest_fn = os.path.join(dest_root, fn)
    return os.path.isfile(dest_root) or os.path.isfile(dest_fn)

def cp_structure_func(source_fn, dest_root, override=True):    
    if dest_exists(source_fn, dest_root) and not override:
        raise FileExistsError(f"dest exists: {source_fn} -> {dest_root}")
    shutil.copy(source_fn, dest_root)





def st_num_structure_func(source_fn, dest_root, override=True):

    st_num_regex = re.compile(r"u\d{8}")

    if not (found := st_num_regex.search(source_fn)):
        raise NameError(f"{source_fn} has no st_number")

    sub_folder = found.group(0)

    base = os.path.join(dest_root, sub_folder)
    try:
        os.makedirs(base)
    except FileExistsError:
        pass

    if dest_exists(source_fn, base) and not override:
        raise FileExistsError(f"dest exists: {source_fn} -> {dest_root}")


    shutil.copy(source_fn, base)


def bulk(source, dest, structure_func=cp_structure_func, override=True, silent_errors=True):

    for root, dirs, files in os.walk(source):
        for fn in files:
            try:
                source_fn = os.path.join(root, fn)
                structure_func(source_fn, dest, override=override,)
            except Exception as e:
                logger.exception(f"Failed structuring {source_fn}", stack_info=True,)
                if not silent_errors:
                    raise
                if isinstance(e, KeyboardInterrupt):
                    raise



def st_num_from(s):
    st_num_regex = re.compile(r"u\d{8}")

    if not (found := st_num_regex.search(s)):
        raise NameError(f"{s} has no st_number")

    return found.group(0)


