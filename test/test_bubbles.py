import json
import numpy as np
import io
import fitz
import pytest
import subprocess
import os 
from frow import ensure_pdf, inspect, merge,  bubbles
from PIL import Image


fixture_path = "test/fixtures/bubble"

score_expected = np.array([
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [1,0,0],
    [0,1,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
])

st_expected = np.array([
    [1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
])

@pytest.mark.parametrize("fn,expected", [
    (os.path.join(fixture_path, "bubbles_score_rot.pdf"), score_expected),
    (os.path.join(fixture_path, "bubbles_score.pdf"), score_expected),
    (os.path.join(fixture_path, "bubbles_st_num.pdf"), st_expected),
    (os.path.join(fixture_path, "bubbles_st_num_red.pdf"), st_expected),
    (os.path.join(fixture_path, "bubbles_st_num_rot.pdf"), st_expected),
    (os.path.join(fixture_path, "bubbles_st_num_rot_shear.pdf"), st_expected),
])
def test_bubbles(fn, expected):

    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    br = bubbles.BubbleReader(im)

    print(br.block_activations)

    assert (br.bubble_matrix == expected).all()
    

@pytest.mark.parametrize("fn", [
    (os.path.join(fixture_path, "no_json.pdf")),
    (os.path.join(fixture_path, "no_qr.pdf")),
])
def test_bubbles_fail(fn):

    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    with pytest.raises(ValueError):
        br = bubbles.BubbleReader(im)
        

@pytest.mark.parametrize("fn", [
    (os.path.join(fixture_path, "no_json_single.pdf")),
])
def test_bubbles_json_fail(fn):

    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    with pytest.raises(json.JSONDecodeError):
        br = bubbles.BubbleReader(im)
                