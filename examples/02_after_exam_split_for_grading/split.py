import os
path, *_ = os.path.split(__file__)

import types
import pathlib

from frow.tools import pdf, qr
from frow.other import pyfunctional_extensions
from functional import seq

import uuid

scan_fns = [pathlib.Path(f"{path}/scan.pdf")]
print(scan_fns)
docs = (seq(scan_fns).map(pdf.open_ensuring_pdf)).list()

mark_recorder = pdf.open_ensuring_pdf(f"{path}/mark_recorder0.pdf")

pages = (seq(docs).map(lambda d: d.pages()).flatten()).list()

# read the id marks on the pages
pages_data = (
    seq(pages).map(
        lambda p: types.SimpleNamespace(
            **{
                "page": p,
                "id_mark_data": (
                    data := qr.read_json_qr(p, relative_rect=(0, 0.6, .3, 1), zoom=2)
                ),
                "doc_id": data.get("doc_id"),
                "page_index": data.get("page_index"),
                "total_pages": data.get("total_pages"),
            }
        )
    )
).list()

# split by page_index and save the split files without any further processing
split_docs = (
    seq(pages_data)    
    .group_by(lambda data: data.page_index)
    .starmap(
        lambda page_index, pages_data: (
            page_index,
            pdf.doc_from_pages(d.page for d in pages_data),
        )
    )
    .star_chained_for_each(lambda page_index, doc: doc.save(f"{path}/raw_split/{page_index}.pdf"))
).list()

# refit the pages and add a mark_recorder 
(    
    seq(split_docs)
    .starmap(
        lambda page_index, doc: (
            page_index,
            pdf.refit_pdf(doc, relative_paste_rect=(0,0,.85,.85))
        )
    )
    .star_chained_for_each(
        lambda page_index, doc: (
            page_index,
            pdf.paste_pdf_on_every_page(doc, mark_recorder, relative_rect=(.86,.1,.95,.5))
        )
    )
    .star_chained_for_each(lambda page_index, doc: doc.save(f"{path}/grading_split/{page_index}.pdf"))
    
).list()


