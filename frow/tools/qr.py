import io
import qrcode
import fitz

import numpy as np


def qr_pdf(
    data,
    dimensions=(200, 100),
    qr_relative_rect=(0.5, 0, 1, 1),
    text_relative_rect=(0, 0, 0.5, 1),
    fontsize = 10,
):
    w, h = dimensions

    doc = fitz.open()
    page = doc.newPage(width=w, height=h)

    scaling = np.array([w, h, w, h])    
    qr_rect = np.array(qr_relative_rect) * scaling
    qr_png_data_stream = io.BytesIO()
    qrcode.make(data).save(qr_png_data_stream, format = "png")
    page.insertImage(qr_rect, stream=io.BytesIO(qr_png_data_stream.getvalue()))

    text_rect = np.array(text_relative_rect) * scaling
    page.insertTextbox(text_rect, buffer=data, fontsize=fontsize)

    return doc

