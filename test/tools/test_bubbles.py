import json
import numpy as np
import io
import fitz
import pytest
import subprocess
import os 
from frow.tools import bubbles
from PIL import Image


fixture_path = "test/fixtures/bubble"
templates_path = "templates"


@pytest.mark.parametrize("fn", [
    os.path.join(templates_path, "st_bubbles_left.pdf"),
    os.path.join(templates_path, "st_bubbles_right.pdf"),
    os.path.join(templates_path, "st_bubbles_up.pdf"),
    os.path.join(templates_path, "st_bubbles_down.pdf"),
])
def test_cropped_bubble_array(tmp_path, fn, ):

    doc = fitz.open(fn)
    matrix = fitz.Matrix(4, 4)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    br = bubbles.BubbleReader(im)

    # br.cropped_bubble_array.show()
    


st_expected = np.array([
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
])

@pytest.mark.parametrize("fn,expected,zoom", [
    (os.path.join(fixture_path, "a.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "b.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "c.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "d.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "e.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "f.pdf"), st_expected, 5),
])
def test_bubble_matrix(fn, expected, zoom):

    doc = fitz.open(fn)
    matrix = fitz.Matrix(zoom, zoom)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    br = bubbles.BubbleReader(im)

    print(br.bubble_matrix)
    assert (br.bubble_matrix == expected).all()
    

    
    
    
    