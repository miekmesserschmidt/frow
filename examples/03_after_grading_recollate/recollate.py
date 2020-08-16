import os
path, *_ = os.path.split(__file__)

import numpy as np
import types
import pathlib
import itertools

from frow.tools import pdf, qr, bubbles
from frow.other import pyfunctional_extensions
from functional import seq

import uuid


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
docs = (seq(scan_fns).map(pdf.open_ensuring_pdf)).list()
pages = (seq(docs).map(lambda d: d.pages()).flatten()).list()

# read the id_mark and score bubbles on each page.
pages_data = (
    seq(pages)
    .map(
        lambda p: types.SimpleNamespace(
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
    )
    .with_progress(len(pages))
).list()

# create a map from a doc_id to a student id
doc_id_to_st_id = dict(
    seq(pages_data)
    .with_progress(len(pages_data))
    .filter(lambda pdata: pdata.page_index == 0)
    .map(lambda pdata: (pdata.doc_id, student_id(pdata.page)))
)

# recollate each student's pages
(
    seq(pages_data)
    .group_by(lambda dpata: dpata.doc_id)
    .starmap(
        lambda doc_id, pdata: (
            doc_id,
            pdf.doc_from_pages(
                d.page for d in 
                sorted(pdata, key=lambda d: d.page_index)
            ),
        )
    )
    .star_chained_for_each(lambda doc_id, doc : doc.save(f"{path}/recollated/{doc_id_to_st_id[doc_id]}.pdf"))
).list()


# calculate the grades and save to a csv
(
    seq(pages_data)
    .group_by(lambda dpata: dpata.doc_id)
    .starmap(
        lambda doc_id, pdata: itertools.chain(
            (doc_id_to_st_id[doc_id], doc_id),
            (d.score for d in sorted(pdata, key=lambda d: d.page_index)),
            tuple([sum(d.score for d in pdata)]),
        )
    )
).to_csv(f"{path}/grades.csv")

