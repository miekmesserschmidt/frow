import os

path, *_ = os.path.split(__file__)

import afterburn
from tqdm import tqdm
from frow.tools import common, pdf


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

# Paste the student number bubbles and id marks and save the documents
a = afterburn.AfterBurn(fns)
(
    a.map(pdf.open_ensuring_pdf, a._)
    .enumerate(a._)    
    .lazy_starapply(add_student_number_bubbles)
    .lazy_starapply(add_page_id_marks)
    .lazy_starapply(save)    
    .tqdm(a._)
    .consume()
)



all_exams = pdf.merge_pdf( doc for id_, doc in a._)
all_exams.save(f"{path}/serial_numbered_pdfs/all.pdf")

