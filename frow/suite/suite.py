from frow.tools import pdf, common, qr
from contextlib import suppress
import subprocess
import re
import os

from . import page_marks


def extract_first_st_num(s):
    st_num_regex = re.compile(r"u\d{8}")

    if not (found := st_num_regex.search(s)):
        raise ValueError(f"{s} has no st_number")

    return found.group(0)


def _extract_fn_from_path(path):
    _, fn = os.path.split(path)
    return fn


def ensure_path(path):
    with suppress(FileExistsError):
        os.makedirs(path)


def fix_broken_pdf(fn, output_path, out_fn=None):
    ensure_path(output_path)
    out_fn = _extract_fn_from_path(fn) if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    command_list = ['pdftocairo', '-pdf', fn, full_out_path]
    p1 = subprocess.call(command_list)

    return full_out_path

def key_merge(key, fn_list, output_path, out_fn=None):
    ensure_path(output_path)
    out_fn = key if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    docs = [pdf.open_ensuring_pdf(fn) for fn in fn_list]
    out_doc = pdf.merge_pdf(docs)
    out_doc.save(full_out_path)
    return full_out_path


def refit(fn, output_path, out_fn=None, rect=(0, 0, 0.85, 0.85)):
    ensure_path(output_path)
    out_fn = _extract_fn_from_path(fn) if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    doc = pdf.open_ensuring_pdf(fn)
    refitdoc = pdf.refit_pdf(doc, relative_paste_rect=rect)
    refitdoc.save(full_out_path)
    return full_out_path


def paste_markrecorder(
    fn,
    output_path,
    bubble_path=page_marks.bubble_array_path,
    out_fn=None,
    rect=(0.87, 0.03, 0.98, 0.5),
):
    ensure_path(output_path)
    out_fn = _extract_fn_from_path(fn) if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    mark_rec = pdf.open_ensuring_pdf(bubble_path)
    doc = pdf.open_ensuring_pdf(fn)
    out_doc = pdf.paste_pdf_on_every_page(doc, mark_rec, relative_rect=rect)

    out_doc.save(full_out_path)
    return full_out_path


def grind_through_image(
    fn, output_path, tmp_path, density=300, width=1500, out_fn=None
):
    ensure_path(output_path)
    out_fn = _extract_fn_from_path(fn) if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    full_tmp_root = os.path.join(tmp_path, out_fn)
    ensure_path(full_tmp_root)
    

    command0 = f"pdftoppm -jpeg -r {density} -scale-to-x {width} -scale-to-y {int(1.4142*width)} {fn} {full_tmp_root}/{out_fn}"
    print(command0)
    p0 = subprocess.call(command0.split())

    command1 = f"convert {full_tmp_root}/*.jpg {full_out_path}.pdf"
    print(command1)
    p1 = subprocess.call(command1.split())

    return f"{full_out_path}.pdf"



def pdf_to_images(
    fn, output_path, density=300, width=1500, out_fn=None
):
    name = _extract_fn_from_path(fn) 
    out_path = os.path.join(output_path, name)
    ensure_path(out_path)

  
    command0 = f"pdftoppm -jpeg -r {density} -scale-to-x {width} -scale-to-y {int(1.4142*width)} {fn} {out_path}/{name}"
    print(command0)
    p0 = subprocess.call(command0.split())

    return out_path


def images_to_pdf(
    path, output_path, density=300, width=1500, out_fn=None, files="*.jpg"
):
    ensure_path(output_path)
    
    name = _extract_fn_from_path(path) 
    out_path = os.path.join(output_path, name)

    command1 = f"convert {path}/{files} {out_path}.pdf"
    print(command1)
    p1 = subprocess.call(command1.split())

    return f"{out_path}.pdf"
  

def add_page_id_marks(
    fn,
    data_dict,
    output_path,
    out_fn=None,
    rect=(0.05, 0.88, 0.5, 0.96),
    add_page_indices=True,
):
    ensure_path(output_path)
    out_fn = _extract_fn_from_path(fn) if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    doc = pdf.open_ensuring_pdf(fn)
    out_doc = common.add_page_id_marks(
        doc, data_dict, add_page_indices=add_page_indices, relative_rect=rect
    )

    out_doc.save(full_out_path)
    return full_out_path




def pdftk_flatten(fn, output_path, out_fn=None):
    ensure_path(output_path)
    out_fn = _extract_fn_from_path(fn) if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    command = f'pdftk {fn} output {full_out_path} flatten'
    p1 = subprocess.call(command.split())
    
    return full_out_path


def write_marks(fn, output_path, out_fn=None, rect=(0.8, 0, 1, 0.7)):
    ensure_path(output_path)
    out_fn = _extract_fn_from_path(fn) if out_fn is None else out_fn
    full_out_path = os.path.join(output_path, out_fn)

    doc = pdf.open_ensuring_pdf(fn)
    for p in doc.pages():
        page_total, _ = page_marks.read_bubble_array(p, rect)
        pdf.place_text(p, str(page_total), relative_rect=(0.9, 0, 1, 0.1))

    doc.save(full_out_path)
    return full_out_path


def read_id_marks(fn, rect=(0, 0.8, 0.4, 1)):

    doc = pdf.open_ensuring_pdf(fn)
    id_data = [page_marks.read_page_id_mark(p, rel_rect=rect) for p in doc.pages()]

    return (fn, id_data)


def read_bubble_array(fn, rect=(0.8, 0, 1, 0.7)):

    doc = pdf.open_ensuring_pdf(fn)
    score_data = [page_marks.read_bubble_array(p, rect) for p in doc.pages()]
    page_totals, page_letters = zip(*score_data)

    return (fn, page_totals, page_letters)


def read_full(fn):
    _, id_data = read_id_marks(fn)
    _, page_totals, page_letters = read_page_marks(fn)

    return (fn, page_totals, page_letters)
