import io
import qrcode
import fitz

from pyzbar.pyzbar import decode
import numpy as np
from PIL import Image

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



def grab_qr_codes(fitz_page, relative_window_rect=None, zoom=2):
    old_crop = fitz_page.CropBox

    page_rect = np.array(fitz_page.bound())
    w = page_rect[2] - page_rect[0]
    h = page_rect[3] - page_rect[1]
    scale = np.array([w,h,w,h])


    if not relative_window_rect:
        abs_window_rect = page_rect
    else:
        abs_window_rect = np.array(relative_window_rect) * scale


    fitz_page.setCropBox(abs_window_rect)

    matrix = fitz.Matrix(zoom, zoom)
    data = fitz_page.getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))
    qr_codes = decode(im)

    fitz_page.setCropBox(old_crop)

    return qr_codes

    


