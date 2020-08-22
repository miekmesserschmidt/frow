import os

path, *_ = os.path.split(__file__)

from tqdm import tqdm
from frow.tools import qr, pdf, bubbles
import more_itertools
import itertools

import types
import pathlib

import numpy as np

from collections import deque


def consume(it):
    deque(it, maxlen=0)


score_array = np.array(
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


def read_student_id(page0):
    return "".join(
        map(
            str,
            np.argmax(
                bubbles.read(page0, relative_rect=(0.4, 0, 0.8, 0.5), zoom=4), axis=0
            ),
        )
    )


def read_page_data(p):
    return types.SimpleNamespace(
        **{
            "page": p,
            "id_mark_data": (
                data := qr.read_json_qr(p, relative_rect=(0, 0.6, 0.3, 1), zoom=4)
            ),
            "doc_id": data.get("doc_id"),
            "page_index": data.get("page_index"),
            "total_pages": data.get("total_pages"),
            "score_bubbles": (
                b := bubbles.read(p, relative_rect=(0.8, 0, 1, 0.5), zoom=4)
            ),
            "score": float(np.sum(b * score_array)),
        }
    )


scan_fns = list(pathlib.Path(f"{path}/graded").glob("*.pdf"))


docs = list(map(pdf.open_ensuring_pdf, scan_fns))
_ = (d.pages() for d in docs)
_ = more_itertools.flatten(_)
pages = list(_)

# Collect the id_mark info
pages_data = list(read_page_data(p) for p in tqdm(pages))

# create a map from a doc_id to a student id
doc_id_to_st_id = dict(
    (pd.doc_id, read_student_id(pd.page))
    for pd in tqdm(pages_data)
    if pd.page_index == 0
)

# create a map from a doc_id to pages data
_ = more_itertools.bucket(tqdm(pages_data), key=lambda pd: pd.doc_id)
doc_id_to_pages = dict((doc_id, list(_[doc_id])) for doc_id in _)

# recollate each student's pages
_ = (
    (doc_id, sorted(pages_data, key=lambda d: d.page_index))
    for doc_id, pages_data in doc_id_to_pages.items()
)
_ = (
    (doc_id, pdf.doc_from_pages(d.page for d in pages_data)) for doc_id, pages_data in _
)
_ = (doc.save(f"{path}/recollated/{doc_id_to_st_id[doc_id]}.pdf") for doc_id, doc in _)
consume(tqdm(_))


# calculate the grades to save to a csv
_ = (
    list(
        itertools.chain(
            (doc_id_to_st_id[doc_id], doc_id),
            (d.score for d in sorted(pages_data, key=lambda d: d.page_index)),
            tuple([sum(d.score for d in pages_data)]),
        )
    )
    for doc_id, pages_data in doc_id_to_pages.items()
)
grades = list(tqdm(_))
print(grades)
