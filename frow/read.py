import numpy as np
import fitz
import io
from pyzbar.pyzbar import decode
from PIL import Image
import json

def read_qr(pil_image, ):
    return decode(pil_image)

def read_json_qr(pil_image, ):
    qr_list = read_qr(pil_image)
    for qr in qr_list:
        try:
            json.loads(qr.data)
            yield qr
        except json.JSONDecodeError:
            pass
    

def read_bubbles(pil_image):
    qrcodes = read_json_qr(pil_image)



    matrix = fitz.Matrix(zoom, zoom)
    data = fitz_page.getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    return decode(im)


def get_bubble_matrix(qr_data, pil_image):

    bubbles_json = json.loads(qr_data.data)
    grid_w, grid_w = bubbles_json.get("grid_w"),  bubbles_json.get("grid_h")
    scale = bubbles_json.get("scale")

    tl, bl, br, tr = qr_data.polygon

    y_unit = (np.array(tl) - np.array(bl) ) / scale
    x_unit = (np.array(tr) - np.array(rl) ) / scale

    

    


    

