import os

path, *_ = os.path.split(__file__)

import afterburn
from tqdm import tqdm
from frow.tools import qr, pdf
import more_itertools
import itertools

import types
import pathlib





scan_fns = [pathlib.Path(f"{path}/scan.pdf")]
mark_recorder = pdf.open_ensuring_pdf(f"{path}/mark_recorder0.pdf")

a = afterburn.AfterBurn(scan_fns)

# Load scans and burst pages
(
    a.map(pdf.open_ensuring_pdf, a._)
    .list(a._)
    .walrus(_docs := a._)
    .generator(doc.pages() for doc in a._)
    .more_itertools.flatten(a._)
    .tqdm(a._)
    .list(a._)
    .walrus(_pages := a._)
)

# Collect the id_mark info
(
    a.generator(
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
        for p in _pages
    )
    .tqdm(a._)
    .list(a._)
    .walrus(_pages_data:=a._)
)

# Bucket pages and save the documents
(
    a.more_itertools.bucket(_pages_data, key=lambda pd: pd.page_index)
    .dict((page_index, a._[page_index]) for page_index in a._)
    .generator(
        pdf.doc_from_pages(d.page for d in pages_data).save(
            f"{path}/raw_split/{page_index}.pdf"
        )
        for page_index, pages_data in a._.items()
    )
    .tqdm(a._)
    .consume()
)
