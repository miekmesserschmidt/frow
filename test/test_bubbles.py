import numpy as np
import io
import fitz
import pytest
import subprocess
import os 
from frow import ensure_pdf, inspect, merge, read, bubbles
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
    (os.path.join(fixture_path, "bubbles_st_num_rot.pdf"), st_expected),
    (os.path.join(fixture_path, "bubbles_st_num_rot_shear.pdf"), st_expected),
])
def test_bubbles(fn, expected):

    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    qr_data = list(read.read_json_qr(im), )[0]
    br = bubbles.BubbleReader(im, qr_data)

    assert (br.bubble_matrix == expected).all()
    