import io
import json
import itertools
import fitz
import qrcode
import numpy as np


def make_bubble_array(
    grid_shape=(10, 10), padding=0.1, scale=20, color=0.8,
):
    """Creates a bubble array.

    Args:
        grid_shape (tuple, optional): Shape of the bubble array. Defaults to (10, 10).
        padding (float, optional): Padding for each cell. Defaults to 0.1.
        scale (int, optional): size of a cell. Defaults to 20.
        color (float, optional): Color used for the bubbles (See fitz colors). Defaults to 0.8.

    Returns:
        [fitz doc]: a fitz pdf doc 
    """
    d = fitz.open()
    w, h = grid_shape

    page = d.newPage(width=w * scale, height=h * scale)

    rect = np.array([0, 0, 1, 1]) * scale
    x_unit = np.array([1, 0, 1, 0]) * scale
    y_unit = np.array([0, 1, 0, 1]) * scale
    padding_offset = np.array([padding, padding, -padding, -padding]) * scale

    for (i, j) in itertools.product(range(w), range(h)):
        page.drawOval(rect + i * x_unit + j * y_unit + padding_offset, color=color)

    return d


def insert_text_array(
    fitz_page, text_array, fontsize=11, color=0.8, scale=20, offset=(7, 14)
):
    """Inserts a 2-d array of strings onto a fitz page at regular intervalse

    Args:
        fitz_page ([fitz page]): Page to insert text array on
        text_array ([2d-str array]): Text array
        fontsize (int, optional):  Defaults to 11.
        color (float, optional):  Defaults to 0.8.
        scale (int, optional): Size of a cell. Defaults to 20.
        offset (tuple, optional):  Defaults to (7, 14).
    """

    x_unit = np.array([1, 0]) * scale
    y_unit = np.array([0, 1]) * scale

    offset = np.array(offset)

    for j, row in enumerate(text_array):
        for i, s in enumerate(row):
            if s:
                pt = i * x_unit + j * y_unit + offset
                fitz_page.insertText(pt, s, fontsize=fontsize, color=color)


def make_qr_data(
    type_="bubble", name=None, grid_shape=(10, 10), qr_span=4, array_position="right"
):
    """Create a data_dict for 

    Args:
        type_ (str, optional): [description]. Defaults to "bubble".
        name ([type], optional): [description]. Defaults to None.
        grid_shape (tuple, optional): [description]. Defaults to (10, 10).
        qr_span (int, optional): [description]. Defaults to 4.
        array_position (str, optional): [description]. Defaults to "right".

    Returns:
        [dict]: 
    """
    return {
        "type": type_,
        "name": name,
        "array_position": array_position,
        "grid_shape": grid_shape,
        "qr_span": qr_span,
    }


def make_bubble_recorder(qr_data, array_fitz_doc):
    """Create a fitz doc containing a bubble recorder.

    Args:
        qr_data ([dict]): output of make_qr_data
        array_fitz_doc ([fitz doc]): output of make_bubble_array

    Returns:
        [fitz doc]: combined orientation qr code and bubble array.
    """

    position = qr_data["array_position"]
    span = qr_data["qr_span"]
    grid_w, grid_h = qr_data["grid_shape"]
    *_, array_w, array_h = array_fitz_doc[0].rect

    a = array_w / grid_w
    b = array_h / grid_h

    qr_w = span * a
    qr_h = span * b

    if position in ("left", "right"):
        recorder_w = max((qr_w + array_w, qr_w, array_w))
        recorder_h = max((qr_h, array_h))
    if position in ("up", "down"):
        recorder_w = max((qr_w, array_w))
        recorder_h = max((qr_h + array_h, qr_h, array_h))

    if position == "left":
        arr_rect = (0, 0, array_w, array_h)
        qr_rect = (array_w, 0, array_w + qr_w, qr_h)

    if position == "right":
        arr_rect = (qr_w, 0, array_w + qr_w, array_h)
        qr_rect = (0, 0, qr_w, qr_h)

    if position == "up":
        arr_rect = (0, 0, array_w, array_h)
        qr_rect = (0, array_h, qr_w, qr_h + array_h)

    if position == "down":
        arr_rect = (0, qr_h, array_w, array_h + qr_h)
        qr_rect = (0, 0, qr_w, qr_h)

    qr_png_data_stream = io.BytesIO()
    qrcode.make(json.dumps(qr_data), border=0).save(qr_png_data_stream, format="png")

    d = fitz.open()
    page = d.newPage(width=recorder_w, height=recorder_h)
    page.insertImage(qr_rect, stream=qr_png_data_stream)
    page.showPDFpage(arr_rect, array_fitz_doc)

    return d

