import os

path, *_ = os.path.split(__file__)

from tqdm import tqdm
from frow.tools import common, pdf

from collections import deque

def consume(it):
    deque(it, maxlen=0)

st_num_bubbles = pdf.open_ensuring_pdf(f"{path}/student_id_bubbles_extra.pdf")

N = 10
fn = f"{path}/blank_exam.pdf"
fns = [fn] * N



def add_student_number_bubbles(id_, doc):
    return pdf.paste_pdf_on(doc[0], st_num_bubbles, relative_rect=(0.5, 0.06, 0.9, 0.3))

def add_page_id_marks(id_, doc):
    return common.add_page_id_marks(
        doc, {"doc_id": id_}, relative_rect=(0.05, 0.9, 0.25, 0.95)
    )
    
def save(id_, doc):
    doc.save(f"{path}/serial_numbered_pdfs/{id_}.pdf")
    
_ = [pdf.open_ensuring_pdf(fn) for fn in fns]
consume(add_student_number_bubbles(id_, doc) for id_,doc in enumerate(tqdm(_)))
consume(add_page_id_marks(id_, doc) for id_,doc in enumerate(tqdm(_)))
consume(save(id_, doc) for id_,doc in enumerate(tqdm(_)))



all_exams = pdf.merge_pdf( doc for id_, doc in enumerate(tqdm(_)))
all_exams.save(f"{path}/serial_numbered_pdfs/all.pdf")

