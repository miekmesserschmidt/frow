import io
import fitz
import pytest
import subprocess
import os 
from frow import ensure_pdf, inspect, merge, read
from PIL import Image


fixture_path = "test/fixtures/bubble"


@pytest.mark.parametrize("fn,expected", [
    (os.path.join(fixture_path, "normal.pdf"), 2),
    (os.path.join(fixture_path, "rotated.pdf"), 2 ),  
    (os.path.join(fixture_path, "rotated_and_sheared.pdf"), 2),
    (os.path.join(fixture_path, "no_json.pdf"),  5),
    (os.path.join(fixture_path, "bubbles.pdf"),  6),
])
def test_read_qr(fn, expected):
    
    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    qr_list = read.read_qr(im)
    assert len(qr_list) == expected

    

@pytest.mark.parametrize("fn,expected", [
    (os.path.join(fixture_path, "normal.pdf"), 2),
    (os.path.join(fixture_path, "rotated.pdf"), 2 ),  
    (os.path.join(fixture_path, "rotated_and_sheared.pdf"), 2),
    (os.path.join(fixture_path, "no_json.pdf"),  0),
    (os.path.join(fixture_path, "bubbles.pdf"),  6),
])
def test_read_json_qr(fn,expected):
    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    qr_list = list(read.read_json_qr(im), )
    assert len(qr_list) == expected

    

@pytest.mark.parametrize("fn", [
    os.path.join(fixture_path, "no_json.pdf"),    
])
def test_read_json_qr_fail_(fn):
    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    qr_list = list(read.read_json_qr(im))

    assert len(qr_list) == 0
    

