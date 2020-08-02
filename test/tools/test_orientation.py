import fitz
import os, pytest
from frow.tools import orientation

fixture_path = "test/fixtures/orientation"

def test_orientation_vec_from_qr():

    fn = "test/fixtures/orientation/tr.pdf"

    doc = fitz.open(fn)
    v = orientation.orientation_vector_from_qr(doc[0],)

    expected = (0,1,0,0)

    assert (v == expected).all()

