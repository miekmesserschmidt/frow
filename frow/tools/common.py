import os
import json
from . import pdf, qr
from ..other import box
import more_itertools

def add_page_id_marks(
    fitz_doc,
    data_dict,
    add_page_indices=True,
    relative_rect=None,
    absolute_rect=None,
    qr_kwargs={},
    paste_kwargs={},
):
    """Adds a page id mark to every page of the document

    Args:
        fitz_doc : Fitz document to add id marks to
        data_dict ([dict]): Data that forms part of the id mark
        add_page_indices (bool, optional): Should page indices form part of the id marks. Defaults to True.
        relative_rect ([type], optional): Relative rectangle to place the id marks. Defaults to None.
        absolute_rect ([type], optional): Absolute rectangle to place the id marks. Defaults to None.
        qr_kwargs (dict, optional): Keyword arguments passed to qr_pdf. Defaults to {}.
        paste_kwargs (dict, optional): Keyword arguments passed to paste. Defaults to {}.

    Returns:
        Fitz doc
    """
    

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

