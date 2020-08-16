import os
path, *_ = os.path.split(__file__)

from frow.tools import common, pdf
from frow.other import pyfunctional_extensions
from functional import seq


st_num_bubbles = pdf.open_ensuring_pdf(f"{path}/student_id_bubbles_extra.pdf")

N = 10
fn = f"{path}/blank_exam.pdf"
fns = [fn] * N

docs = (    
    seq(fns)    
    .map(pdf.open_ensuring_pdf)        
    .chained_for_each(
        lambda doc: pdf.paste_pdf_on(
            doc[0], st_num_bubbles, relative_rect=(0.5, 0.06, 0.9, 0.3)
        )
    )
    .enumerate()
    .with_progress(N)    
    .star_chained_for_each(
        lambda id_, doc: common.add_page_id_marks(
            doc, {"doc_id": id_}, relative_rect=(0.05, 0.9, 0.25, 0.95)
        )
    )    
    .star_chained_for_each(
        lambda id_, doc: doc.save(
            f"{path}/serial_numbered_pdfs/{id_}.pdf"
        )
    )
    
    
).list()

all_exams = pdf.merge_pdf(doc for id_, doc in docs)
all_exams.save(f"{path}/serial_numbered_pdfs/all.pdf")