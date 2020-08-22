import os

path, *_ = os.path.split(__file__)

from tqdm import tqdm
from frow.tools import qr, pdf
import more_itertools
import itertools

import types
import pathlib
from collections import deque


def consume(it):
    deque(it, maxlen=0)


scan_fns = [pathlib.Path(f"{path}/scan.pdf")]
mark_recorder = pdf.open_ensuring_pdf(f"{path}/mark_recorder0.pdf")


# Load scans and burst pages
docs = list(map(pdf.open_ensuring_pdf, scan_fns))
_ = list(d.pages() for d in docs)
pages = list(more_itertools.flatten(tqdm(_)))


# Collect the id_mark info
pages_data = list(
    types.SimpleNamespace(
        **{
            "page": p,
            "id_mark_data": (
                data := qr.read_json_qr(p, relative_rect=(0, 0.6, 0.3, 1), zoom=2)
            ),
            "doc_id": data.get("doc_id"),
            "page_index": data.get("page_index"),
            "total_pages": data.get("total_pages"),
        }
    )
    for p in tqdm(pages)
)

_ = more_itertools.bucket(pages_data, key=lambda pd: pd.page_index)
_ = dict((page_index, _[page_index]) for page_index in _)
consume(
    pdf.doc_from_pages(d.page for d in pages_data).save(
        f"{path}/raw_split/{page_index}.pdf"
    )
    for page_index, pages_data in tqdm(_.items())
)
