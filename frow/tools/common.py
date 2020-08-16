import json
from . import pdf, qr
from ..other import box


def add_page_id_marks(
    fitz_doc,
    data_dict,
    add_page_indices=True,
    relative_rect=None,
    absolute_rect=None,
    qr_kwargs={},
    paste_kwargs={},
):
    # TODO docstring

    for i, page in enumerate(fitz_doc.pages()):
        d = {
            "type": "id_mark",
        }
        d.update(data_dict)
        if add_page_indices:
            d.update(
                {"page_index": i, "total_pages": fitz_doc.pageCount,}
            )

        qr_pdf = qr.qr_pdf(json.dumps(d), **qr_kwargs)

        pdf.paste_pdf_on(
            page,
            qr_pdf,
            relative_rect=relative_rect,
            absolute_rect=absolute_rect,
            **paste_kwargs
        )

    return fitz_doc

