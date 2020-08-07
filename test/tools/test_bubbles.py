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

real_expected1 = np.array([
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,0,0],
])


real_expected2 = np.array([
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,0,0],
])

@pytest.mark.parametrize("fn,expected,zoom", [
    (os.path.join(fixture_path, "a.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "d.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "b.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "c.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "e.pdf"), st_expected, 2),
    (os.path.join(fixture_path, "f.pdf"), st_expected, 5),

    (os.path.join(fixture_path, "real_pg_0001.pdf"), real_expected1, 4),
    (os.path.join(fixture_path, "real_pg_0002.pdf"), real_expected2, 4),
    (os.path.join(fixture_path, "real_pg_0003.pdf"), real_expected2, 4),
    (os.path.join(fixture_path, "real_pg_0004.pdf"), real_expected2, 4),
    (os.path.join(fixture_path, "real_pg_0005.pdf"), real_expected2, 4),
    (os.path.join(fixture_path, "real_pg_0006.pdf"), real_expected2, 3),

    (os.path.join(fixture_path, "real_photo.pdf"), real_expected2, 3),
    
    # (os.path.join(fixture_path, "shadowed.pdf"), real_expected2, 3),
    # (os.path.join(fixture_path, "real_dirty.pdf"), real_expected2, 3),

])
def test_bubble_matrix(fn, expected, zoom):

    doc = fitz.open(fn)
    matrix = fitz.Matrix(zoom, zoom)
    data = doc[0].getPixmap(matrix=matrix).getImageData()
    im = Image.open(io.BytesIO(data))

    br = bubbles.BubbleReader(im)

    # br.cropped_bubble_array.show()
    # br.block_processed_bubble_array.show()
    # br.cropped_bubble_array.show()


    print("\n", br.block_activations)
    print("\n", np.argmax(br.block_activations, axis=0))

    # print("median ", np.median(br.block_activations))
    # print("mean ",np.mean(br.block_activations))
    # print("max ",np.max(br.block_activations))
    # print("min ",np.min(br.block_activations))
    assert (br.bubble_matrix() == expected).all()
    
