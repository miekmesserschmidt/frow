import itertools
import os
import fitz
import shutil
import tqdm
import pathlib

def merge(source_list, dest):
    b = fitz.open()

    for source_fn in source_list:
        a = fitz.open(source_fn)
        b.insertPDF(a)

    b.save(dest)



def subfolder_merge(source, dest):
    for root, dirs, files in os.walk(source):

        if not files:
            continue


        sources = sorted([os.path.join(root, fn) for fn in files])

        parent = os.path.split(root)[-1]
        dest_fn = os.path.join(dest, f"{parent}.pdf")

        merge(sources, dest_fn)
