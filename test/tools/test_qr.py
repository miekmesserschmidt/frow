import io
import fitz
from PIL import Image
import subprocess
import os
import pytest
from frow.tools import qr
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



