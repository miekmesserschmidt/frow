import json
import subprocess
import fitz
import os, pytest
from frow.tools import orientation, pdf, qr

fixture_path = "test/fixtures/orientation"


@pytest.mark.parametrize(
    "fn, expected",
    [
        (os.path.join(fixture_path, "tl.pdf"), (1, 0, 0, 0)),
        (os.path.join(fixture_path, "tr.pdf"), (0, 1, 0, 0)),
        (os.path.join(fixture_path, "br.pdf"), (0, 0, 1, 0)),
        (os.path.join(fixture_path, "bl.pdf"), (0, 0, 0, 1)),
    ],
)
def test_orientation_vec_from_qr(fn, expected):

    doc = fitz.open(fn)
    v = orientation.orientation_vector_from_qr(doc[0],relative_window=(0,0,.5,.5))

    assert (v == expected).all()


@pytest.mark.parametrize(
    "fn",
    [
        os.path.join(fixture_path, "tl.pdf"),
        os.path.join(fixture_path, "tr.pdf"),
        os.path.join(fixture_path, "br.pdf"),
        os.path.join(fixture_path, "bl.pdf"),
    ],
)
def test_orient_page(tmp_path, fn):

    correct_orientation = (1, 0, 0, 0)

    doc = fitz.open(fn)
    v = orientation.orientation_vector_from_qr(doc[0], relative_window=(0,0,.5,.5))
    orientation.orient_page(doc[0], v, correct_orientation)
    doc = pdf.svg_plonk(doc)

    oriented_fn = os.path.join(tmp_path, "oriented_fn.pdf")
    doc.save(oriented_fn)

    doc_out = fitz.open(oriented_fn)
    out_v = orientation.orientation_vector_from_qr(doc_out[0],relative_window=(0,0,.5,.5))
    assert (out_v == correct_orientation).all()




@pytest.mark.parametrize(
    "paste_pos",
    [
        (0,0,.25,.25), # top left
        (.75,0,1,.25), # top right
        (.75,.75,1,1), # bottom right
        (0,.75,.25,1), # bottom left
    ],
)
def test_by_id_mark(tmp_path, paste_pos):


    doc = fitz.open()
    p = doc.newPage()
   
    mark = qr.qr_pdf(json.dumps({"type" : "id_mark", "doc_id":"4444"}))
    pdf.paste_pdf_on(p, mark, relative_rect=paste_pos)
    
    orientation.orient_by_id_mark(p, relative_window=(0,0,.5,.5))
    
    outd = pdf.svg_plonk(doc)
    
    # import uuid
    # import subprocess
    # outfn = os.path.join(tmp_path, str(uuid.uuid1()))
    # outd.save(outfn)
    # subprocess.call(["xdg-open", outfn])
    
    d = qr.read_json_qr(outd[0], relative_rect=(0,.5,.5,1),zoom=2)
    assert d
    

