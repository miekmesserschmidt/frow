import json
from ..tools import pdf_transform, qr, box


def page_data(doc_id, page_index, total_pages):
    return json.dumps(
        {
            "type": "page_id_mark",
            "doc_id": doc_id,
            "page_index": page_index,
            "total_pages": total_pages,
        }
    )


def add_page_id_marks(
    fitz_doc,
    doc_id,
    relative_rect=None,
    absolute_rect=None,
    page_data_gen=page_data,
    qr_kwargs={},
    paste_kwargs={},
): 
    #TODO docstring

    for i, page in enumerate(fitz_doc.pages()):
        data = page_data_gen(doc_id, i, total_pages=fitz_doc.pageCount)
        qr_pdf = qr.qr_pdf(data, **qr_kwargs)

        pdf_transform.paste_pdf_on(
            page,
            qr_pdf,
            relative_rect=relative_rect,
            absolute_rect=absolute_rect,
            **paste_kwargs
        )

    return fitz_doc

