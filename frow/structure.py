import os
import shutil
import re


def cp_structure_func(source_fn, dest_root):
    shutil.copy(source_fn, dest_root)


def st_num_structure_func(source_fn, dest_root):
    st_num_regex = re.compile(r"u\d{8}")

    if not (found := st_num_regex.search(source_fn)):
        raise NameError(f"{source_fn} has no st_number")

    print(found)
    sub_folder = found.group(0)

    base = os.path.join(dest_root, sub_folder)
    try:
        os.makedirs(base)
    except FileExistsError:
        pass
    
    shutil.copy(source_fn, base)


def bulk(source, dest, structure_func=cp_structure_func):

    for root, dirs, files in os.walk(source):
        for fn in files:
            source_fn = os.path.join(root, fn)
            structure_func(source_fn, dest)