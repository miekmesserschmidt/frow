import frozendict
import json
import io
import qrcode
import fitz

from pyzbar.pyzbar import decode
import numpy as np
from PIL import Image

from . import box, pdf_transform


def qr_pdf(
    data: str,
    dimensions=(200, 100),
    qr_relative_rect=(0.5, 0, 1, 1),
    text_relative_rect=(0, 0, 0.5, 1),
    fontsize=10,
):
    """Creates a fitz pdf containing a qr_code and its data.

    Args:
        data ([str]): data to encoding into the qr code
        dimensions (tuple, optional): Dimensions of the output. Defaults to (200, 100).
        qr_relative_rect (tuple, optional): Where to place the qr_code in the pdf result. Defaults to (0.5, 0, 1, 1).
        text_relative_rect (tuple, optional): Where to place the text in the pdf result. Defaults to (0, 0, 0.5, 1).
        fontsize (int, optional): Font size of text. Defaults to 10.

    Returns:
        [fitz pdf]: The resulting qr pdf.
    """
    w, h = dimensions
    abs_box = (0, 0, w, h)

    doc = fitz.open()
    page = doc.newPage(width=w, height=h)

    qr_rect = box.absolute_box(qr_relative_rect, abs_box)
    text_rect = box.absolute_box(text_relative_rect, abs_box)

    qr_png_data_stream = io.BytesIO()
    qrcode.make(data, border=0).save(qr_png_data_stream, format="png")
    page.insertImage(qr_rect, stream=qr_png_data_stream)

    page.insertTextbox(text_rect, buffer=data, fontsize=fontsize)

    return doc


def grab_qr_codes(fitz_page, relative_rect=None, absolute_rect=None, zoom=2):
    """Decodes all qr codes in the given rectangle and returns the decoded data.

    Args:
        fitz_page ([fitz page]): page to grab the data from.
        relative_window_rect (4-tuple): Relative rect to grab data from. Defaults to None. (one of relative_window_rect or abs_window_rect must be None)
        abs_window_rect (4-tuple):  Absolute rect to grab data from. Defaults to None. (one of relative_window_rect or abs_window_rect must be None)
        zoom (int, optional): zoom level for rasterization. Defaults to 2.

    Returns:
        [list]: list of all the qr_codes detected
    """
    im = pdf_transform.crop_to_pillow_image(
        fitz_page, relative_rect=relative_rect, absolute_rect=absolute_rect, zoom=zoom,
    )
    qr_codes = decode(im)

    return qr_codes


def read_json_qr(fitz_page, relative_rect=None, absolute_rect=None, zoom=2):
    codes = grab_qr_codes(
        fitz_page, relative_rect=relative_rect, absolute_rect=absolute_rect, zoom=zoom
    )
    if not codes:
        raise ValueError("No qr codes detected")
    elif len(codes) > 1:
        raise ValueError("Multiple qr-codes detected")

    code = codes[0]    
    s = code.data

    return json.loads(s)

