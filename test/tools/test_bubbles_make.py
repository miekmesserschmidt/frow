import json
import numpy as np
import io
import fitz
import pytest
import subprocess
import os 
from frow.tools.bubbles import make
from frow.tools.bubbles.easy import make as make_easy
from PIL import Image


def test_bubbles_make_array(tmp_path):

    fn = os.path.join(tmp_path, "out.pdf")

    text_array = [[str(i)]*3 for i in range(10)]

    d = make.make_bubble_array(grid_shape=(3,10))
    make.insert_text_array(d[0], text_array)
    d.save(fn)

    # subprocess.call(["xdg-open", fn])


@pytest.mark.parametrize("pos", ["right", "left", "up", "down"])
def test_bubbles_make_recorder(tmp_path, pos):
    

    fn = os.path.join(tmp_path, f"out.{pos}.pdf")

    text_array = [[str(i)]*8 for i in range(10)]
    array_doc = make.make_bubble_array(grid_shape=(8,10))
    make.insert_text_array(array_doc[0], text_array)

    qr_data = make.make_qr_data(grid_shape=(8,10), array_position=pos, qr_span=5)
    d = make.make_bubble_recorder(qr_data, array_doc)
    d.save(fn)

    # subprocess.call(["xdg-open", fn])


@pytest.mark.parametrize("pos", ["right", "left", "up", "down"])
def test_bubbles_make_easy(tmp_path, pos):
    

    fn = os.path.join(tmp_path, f"out.{pos}.pdf")
    

    text_array = [[str(i)]*8 for i in range(10)]
    d = make_easy(grid_shape=(8,10), array_position=pos)
    d.save(fn)

    # subprocess.call(["xdg-open", fn])
