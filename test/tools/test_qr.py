import io
import fitz
from PIL import Image
import subprocess
import os
import pytest
from frow.tools import qr, box
from pyzbar.pyzbar import decode
import functional
import json


@pytest.mark.parametrize("data", 
    [
        "data",
        json.dumps({"type" : "page_info", "doc_id" : "fa3ab3", "page_no" :"1"})
    ]
)
def test_qr_pdf(tmp_path, data):
    doc = qr.qr_pdf(data)
    out_fn = os.path.join(tmp_path, "out.pdf")
    doc.save(out_fn)


    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    decode(im)[0].data == data

    # subprocess.call(["xdg-open", out_fn])



def test_grab_qr_codes_rel(tmp_path, ):

    in_fn = "test/fixtures/bubble/bubbles_st_num_rot.pdf"
    doc = fitz.open(in_fn)
    
    
    bottom_left = (0,.5,.5,1)
    bottom_right = (.5,.5,1,1)
    
    bl_qr = qr.grab_qr_codes(doc[0], relative_window_rect=bottom_left)
    br_qr = qr.grab_qr_codes(doc[0], relative_window_rect=bottom_right)
    whole = qr.grab_qr_codes(doc[0])

    assert len(bl_qr) == 1
    assert len(br_qr) == 0
    assert len(whole) == 1
    # subprocess.call(["xdg-open", out_fn])




def test_grab_qr_codes_abs(tmp_path, ):

    in_fn = "test/fixtures/bubble/bubbles_st_num_rot.pdf"
    doc = fitz.open(in_fn)
    
    
    bottom_left = box.absolute_box((0,.5,.5,1), doc[0].rect)
    bottom_right = box.absolute_box((.5,.5,1,1), doc[0].rect)
    
    bl_qr = qr.grab_qr_codes(doc[0], abs_window_rect=bottom_left)
    br_qr = qr.grab_qr_codes(doc[0], abs_window_rect=bottom_right)
    whole = qr.grab_qr_codes(doc[0])

    assert len(bl_qr) == 1
    assert len(br_qr) == 0
    assert len(whole) == 1
    # subprocess.call(["xdg-open", out_fn])



