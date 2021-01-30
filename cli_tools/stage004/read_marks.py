#! env/bin/python3.8
import os, sys

print(os.getcwd())
conf_path = os.getcwd()
sys.path.append(conf_path)

import csv
import collections
import pathlib
import itertools
import multiprocessing

from tqdm import tqdm
import numpy as np
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
    fn, zoom = input_
    st_num = extract_first_st_num(fn)

    recorder = collections.defaultdict(int)

    d = pdf.open_ensuring_pdf(fn)
    for p in d.pages():
        bubble_array = bubbles.read_robust(p, (0.8, 0, 1, 0.5))
        page_total = np.sum(bubble_array * BUBBLEARRAY)

        qr_data = qr.read_json_qr_robust(p, relative_rect=(0, 0.8, 0.4, 1))

        st_num = qr_data["st_num"]
        q = qr_data["doc_id"]
        index = qr_data["page_index"]

        recorder["st_num"] = st_num
        recorder[q] += page_total
        recorder["pagecount"] += 1

    return recorder


@click.command()
@click.argument("source")
@click.argument("dest")
@click.option("--zoom", "-z", default=1.5, type=float)
@click.option("--processors", "-p", default=10, type=int)
def read_marks(source, dest, zoom, processors):

    fns = [(str(p), zoom) for p in pathlib.Path(source).glob("**/*")]

    records = collections.defaultdict(dict)
    with multiprocessing.Pool(processors) as pool:
        for record in tqdm(
            pool.imap_unordered(worker, fns, chunksize=10), total=len(fns)
        ):
            records[record["st_num"]].update(record)

    headings = set(itertools.chain(*(item.keys() for item in records.values())))

    with open(dest, "w") as f:
        w = csv.DictWriter(f, fieldnames=sorted(headings))
        w.writeheader()
        w.writerows(records.values())


if __name__ == "__main__":
    read_marks()
