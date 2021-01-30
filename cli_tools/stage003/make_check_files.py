#! env/bin/python3.8

import sys, os

print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)


import pprint
from contextlib import suppress
import io
import multiprocessing
import pathlib

import fitz
import numpy as np
from tqdm import tqdm
import click

from frow.other import itools
from frow.tools import pdf, common, qr, bubbles
from frow.up import extract_first_st_num


BUBBLEARRAY = np.array(
    [
        [0, 0.5],
        [10, 1],
        [20, 2],
        [30, 3],
        [40, 4],
        [50, 5],
        [60, 6],
        [70, 7],
        [80, 8],
        [90, 9],
    ]
)


def worker(input_):
    fn, dest = input_
    *_, only_fn = os.path.split(fn)

    in_doc = pdf.open_ensuring_pdf(fn)

    for i, p in enumerate(in_doc.pages()):

        bubble_array = bubbles.read_robust(p, (0.8, 0, 1, 0.5))
        page_total = np.sum(BUBBLEARRAY * bubble_array)
        qr_data = qr.read_json_qr_robust(p, relative_rect=(0, 0.8, 0.4, 1))
        array_image = pdf.crop_to_pillow_image(
            p, relative_rect=(0.85, 0, 1, 0.6), zoom=2
        )

        stream = io.BytesIO()
        array_image.save(stream, format="pdf")
        array_pdf = fitz.open(stream=stream.getvalue(), filetype="pdf")

        out_doc = fitz.open()
        newpage = out_doc.newPage(width=200, height=200)
        pdf.paste_pdf_on(newpage, array_pdf, relative_rect=(0.4, 0, 1, 1))
        pdf.place_text(
            newpage,
            f"{qr_data['st_num']}\n{qr_data['doc_id']}",
            relative_rect=(0.05, 0.1, 0.4, 0.5),
            fontsize=10,
        )
        pdf.place_text(
            newpage,
            pprint.pformat(dict(qr_data)),
            relative_rect=(0.05, 0.4, 0.5, 1),
            fontsize=5,
        )

        out_fn = os.path.join(
            dest,
            f"{page_total:07}.{qr_data['st_num']}.{qr_data['doc_id']}.{qr_data['page_index']:05}.pdf",
        )
        out_doc.save(out_fn)


@click.command()
@click.argument("source")
@click.argument("dest")
@click.option("--processors", "-p", default=10, type=int)
@click.option("--chunksize", "-p", default=1, type=int)
def make_check_files(source, dest, processors, chunksize):

    with suppress(FileExistsError):
        os.makedirs(dest)

    inputs = [(str(p), dest) for p in pathlib.Path(source).glob("**/*") if not p.is_dir()]

    with multiprocessing.Pool(processors) as pool:
        for _ in tqdm(
            pool.imap_unordered(worker, inputs, chunksize=chunksize), total=len(inputs)
        ):
            pass


if __name__ == "__main__":
    make_check_files()
