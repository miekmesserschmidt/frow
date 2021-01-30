#! env/bin/python3.8

import os, sys

print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


import click
import pathlib
import numpy as np
from contextlib import suppress

from tqdm import tqdm

from frow.tools import pdf


@click.command()
@click.argument("source")
@click.argument("dest")
@click.option("--zoom", "-z", default=2, type=float)
def fn_burst(source, dest, zoom):

    with suppress(FileExistsError):
        os.makedirs(dest)

    fns = [str(p) for p in pathlib.Path(source).glob("**/*")]

    for fn in tqdm(fns):
        doc = pdf.open_ensuring_pdf(fn)
        page_docs = [pdf.doc_from_pages([p]) for p in doc.pages()]

        for i, out_doc in enumerate(page_docs):
            _, true_fn = os.path.split(fn)
            out_fn = os.path.join(dest, f"{true_fn}.{i}.pdf")
            out_doc.save(out_fn)


if __name__ == "__main__":
    fn_burst()

