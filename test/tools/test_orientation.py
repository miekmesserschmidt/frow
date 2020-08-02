import fitz
import os, pytest
from frow.tools import orientation

fixture_path = "test/fixtures/orientation"


@pytest.mark.parametrize("fn, expected", [
    (os.path.join(fixture_path, "tl.pdf"), (1,0,0,0)),
    (os.path.join(fixture_path, "tr.pdf"), (0,1,0,0)),
    (os.path.join(fixture_path, "bl.pdf"), (0,0,1,0)),
    (os.path.join(fixture_path, "br.pdf"), (0,0,0,1)),
])
def test_orientation_vec_from_qr(fn, expected):


    doc = fitz.open(fn)
    v = orientation.orientation_vector_from_qr(doc[0],)


    assert (v == expected).all()

