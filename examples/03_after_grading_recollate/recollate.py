import os

path, *_ = os.path.split(__file__)

import afterburn
from tqdm import tqdm
from frow.tools import qr, pdf, bubbles
import more_itertools
import itertools

import types
import pathlib

import numpy as np



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


def student_id(page0):
    return "".join(
        map(
            str,
            np.argmax(
                bubbles.read(page0, relative_rect=(0.4, 0, 0.8, 0.5), zoom=4), axis=0
            ),
        )
    )


scan_fns = list(pathlib.Path(f"{path}/graded").glob("*.pdf"))
a = afterburn.AfterBurn(scan_fns)

(
    a.map(pdf.open_ensuring_pdf, a._)
    .list(a._)
    .walrus(_docs:=a._)
    .generator(doc.pages() for doc in a._)
    .more_itertools.flatten(a._)
    .tqdm(a._)
    .list(a._)
    .walrus(_pages:=a._)
)

# Collect the id_mark info
(
    a.generator(
        types.SimpleNamespace(
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
        for p in _pages
    )
    .tqdm(a._)
    .list(a._)
    .walrus(_pages_data:=a._)
)


# create a map from a doc_id to a student id
doc_id_to_st_id = dict(
    (pd.doc_id, student_id(pd.page)) for pd in _pages_data if pd.page_index == 0
)

# create a map from a doc_id to pages data
doc_id_to_pages = (
    a.more_itertools.bucket(_pages_data, key=lambda pd: pd.doc_id)
    .dict((doc_id, list(a._[doc_id])) for doc_id in a._)
    ._
)


# recollate each student's pages
(
    a.generator(
        pdf.doc_from_pages(
            d.page for d in sorted(pages_data, key=lambda d: d.page_index)
        ).save(f"{path}/recollated/{doc_id_to_st_id[doc_id]}.pdf")
        for doc_id, pages_data in doc_id_to_pages.items()
    )
    .tqdm(a._)
    .consume(a._)
)

# calculate the grades to save to a csv
(
    a.generator(
        itertools.chain(
            (doc_id_to_st_id[doc_id], doc_id),
            (d.score for d in sorted(pages_data, key=lambda d: d.page_index)),
            tuple([sum(d.score for d in pages_data)]),
        )
        for doc_id, pages_data in doc_id_to_pages.items()
    )
    .map(tuple, a._)
    .list(a._)
)
print(a._)
