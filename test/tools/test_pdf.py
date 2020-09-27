import pathlib
import uuid
import fitz
import subprocess
import os
import pytest
from frow.tools import pdf, inspect


def test_refit(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")

    d = fitz.open(fn)

    dd = pdf.refit_pdf(d, relative_paste_rect=(0, 0, 0.8, 0.8))
    dd.save(out)

    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 4

    # subprocess.call(["xdg-open", out])


def test_pdf_paste_on(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    out = os.path.join(tmp_path, "0.pdf")

    doc = fitz.open(fn)
    source_doc = fitz.open(fn)

    pdf.paste_pdf_on(doc[0], source_doc, (0.5, 0.5, 1, 1))

    doc.save(out)

    # subprocess.call(["xdg-open", out])


def test_crop_to_pillow_image(tmp_path):

    fn = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")

    doc = fitz.open(fn)

    rel_rect = (0, 0, 0.5, 0.5)

    im = pdf.crop_to_pillow_image(doc[0], relative_rect=rel_rect, zoom=2)
    # im.show()


def test_merge_pdf(tmp_path):

    out = os.path.join(tmp_path, "0.pdf")
    fn0 = os.path.join("test/fixtures/sub_folder_merge", "a", "0.pdf")
    fn1 = os.path.join("test/fixtures/sub_folder_merge", "a", "1.pdf")

    doc = pdf.merge_pdf(map(fitz.open, [fn0, fn1]))

    doc.save(out)

    # subprocess.call(["xdg-open", out])


@pytest.mark.parametrize(
    "img_fn",
    [
        "test/fixtures/img/00.jpg",
        "test/fixtures/img/00.jpg.pdf",
        "test/fixtures/img/01.jpg",
        "test/fixtures/img/02.jpg",
        "test/fixtures/img/03.jpg",
        "test/fixtures/img/04.png",
        "test/fixtures/img/05.jpg",
        "test/fixtures/img/06.png",
    ],
)
def test_open_ensuring_pdf(tmp_path, img_fn):

    out = os.path.join(tmp_path, f"{uuid.uuid1()}.pdf")

    doc = pdf.open_ensuring_pdf(img_fn)
    doc.save(out)

    assert inspect.is_pdf(out)

    # subprocess.call(["xdg-open", out])


def test_bucket_merge(tmp_path):
    fns = pathlib.Path("test/fixtures/bucket_merge").glob("**/*")
    fns = [str(fn) for fn in fns]
    from frow.up import extract_first_st_num

    pdf.bucket_merge(
        fns, tmp_path, key=extract_first_st_num, out_fn_template="{key}.pdf"
    )

    a = fitz.open(os.path.join(tmp_path, "u00000000.pdf"))
    b = fitz.open(os.path.join(tmp_path, "u00000001.pdf"))

    assert a.pageCount == 2
    assert b.pageCount == 3




def test_bucket_merge_gen(tmp_path):
    fns = pathlib.Path("test/fixtures/bucket_merge").glob("**/*")
    fns = [str(fn) for fn in fns]
    from frow.up import extract_first_st_num

    for key, doc in pdf.bucket_merge_gen(fns, key=extract_first_st_num):
        doc.save(os.path.join(tmp_path, f"{key}.pdf"))

    a = fitz.open(os.path.join(tmp_path, "u00000000.pdf"))
    b = fitz.open(os.path.join(tmp_path, "u00000001.pdf"))

    assert a.pageCount == 2
    assert b.pageCount == 3


def test_place_text(tmp_path):
    fn = "test/fixtures/bubble/real_pg_0001.pdf"
    out = os.path.join(tmp_path, "b.pdf")

    d = fitz.open(fn)

    dd = pdf.place_text(d[0], "lorem", relative_rect=(.2,.2,.3,.3))
    d.save(out)

    assert inspect.is_pdf(out)

    A = fitz.open(out)
    assert A.pageCount == 1

    # subprocess.call(["xdg-open", out])

